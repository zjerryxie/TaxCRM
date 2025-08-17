# -*- coding: utf-8 -*-
"""
TaxCRM AI Chatbot Controller
- Secure web2py integration
- Personalized tax advice
- Audit-compliant responses
"""

from gluon import current, HTTP, redirect, URL
from gluon.tools import Auth, Service
import logging
import re
import time
from datetime import datetime

# Initialize web2py components
auth = current.auth
db = current.db
response = current.response
request = current.request
cache = current.cache

logger = logging.getLogger("web2py.app.taxcrm")
logger.setLevel(logging.INFO)

service = Service()

class TaxChatBot:
    """Core AI tax advisor logic"""
    
    def __init__(self):
        self.max_question_length = 500
        self.sensitive_patterns = [
            r"\d{3}-\d{2}-\d{4}",  # SSN
            r"\d{2}-\d{7}",         # EIN
            r"\b\d{4}\b"            # Last 4 digits
        ]
        
        # Initialize in production with actual keys
        self.openai_key = current.deployment_settings.get('openai.key')
        
    def sanitize_input(self, text):
        """Remove sensitive data before processing"""
        for pattern in self.sensitive_patterns:
            text = re.sub(pattern, "[REDACTED]", text)
        return text.strip()
    
    def get_tax_context(self, user_id):
        """Get user's tax profile using web2py DAL"""
        try:
            context = {
                'personal': db(db.user_profiles.user_id == user_id).select().first(),
                'documents': db(db.tax_documents.user_id == user_id).select(),
                'filing_history': db(db.filing_history.user_id == user_id).select(
                    orderby=~db.filing_history.year,
                    limitby=(0, 3)
            }
            return context
        except Exception as e:
            logger.error(f"Context fetch failed: {e}")
            return None
    
    def generate_response(self, user_id, question):
        """Main response generation pipeline"""
        start_time = time.time()
        
        try:
            # Validate input
            if not question or len(question) > self.max_question_length:
                raise ValueError("Invalid question length")
            
            clean_question = self.sanitize_input(question)
            context = self.get_tax_context(user_id)
            
            if not context:
                raise RuntimeError("Could not load tax context")
            
            # Generate and format response
            answer = self._call_ai_model(clean_question, context)
            processed = self._postprocess(answer, context)
            
            # Log performance
            response_time = time.time() - start_time
            self._log_interaction(
                user_id, question, processed, 
                response_time, context
            )
            
            return processed
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return {
                'answer': "⚠️ System temporarily unavailable. Please try again later.",
                'sources': [],
                'disclaimers': ["Service interruption"],
                'confidence': 0
            }
    
    def _call_ai_model(self, question, context):
        """Call OpenAI with tax-specific prompting"""
        # Implement with your actual AI integration
        return {
            'answer': "Sample tax advice based on your context",
            'sources': ["IRS Pub 17"],
            'confidence': 0.9
        }
    
    def _postprocess(self, response, context):
        """Add compliance disclaimers"""
        if context['personal'].get('high_risk_flag'):
            response['disclaimers'] = [
                "Consult a tax professional for your specific situation"
            ]
        return response
    
    def _log_interaction(self, user_id, question, response, time_sec, context):
        """Store conversation in database"""
        try:
            db.conversation_log.insert(
                user_id=user_id,
                question=question[:500],
                answer=response['answer'][:1000],
                response_time=time_sec,
                context=context.get('personal', {}).get('filing_status'),
                created_on=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Failed to log conversation: {e}")

def chat():
    """AJAX endpoint for chatbot queries"""
    if not auth.user:
        raise HTTP(403, "Authentication required")
    
    try:
        bot = TaxChatBot()
        question = request.vars.question
        
        if not question:
            raise HTTP(400, "Question parameter required")
        
        result = bot.generate_response(
            user_id=auth.user.id,
            question=question
        )
        
        return response.json({
            'status': 'success',
            'data': result,
            'csrf_token': request.csrf_token
        })
        
    except HTTP:
        raise
    except Exception as e:
        logger.exception("Chatbot error")
        raise HTTP(500, "Internal server error")

def index():
    """Main chat interface"""
    if not auth.user:
        redirect(URL('default', 'user/login'))
    
    return dict(
        chat_endpoint=URL('ai_chatbot', 'chat'),
        max_length=500
    )

# Web2py URL routing
def __call__():
    """Handle different request types"""
    return service()
