# -*- coding: utf-8 -*-
"""
TaxCRM AI Chat Model
- Business logic for tax advice generation
- Database abstractions
- Compliance checks
"""

from gluon import current
from gluon.tools import Auth
import logging
import re
import json
from datetime import datetime

# Initialize web2py components
db = current.db
auth = current.auth
cache = current.cache
logger = logging.getLogger("web2py.app.taxcrm_ai")

class TaxAIModel:
    """Core AI tax advisor business logic"""
    
    def __init__(self):
        self.max_history = 3  # Number of past returns to consider
        self.risk_threshold = 0.7  # Confidence threshold for warnings
        
    def get_tax_context(self, user_id):
        """
        Retrieve complete tax context for a user
        Returns: {
            'profile': {...},
            'documents': [...],
            'history': [...],
            'family': [...]
        }
        """
        try:
            context = {
                'profile': self._get_user_profile(user_id),
                'documents': self._get_current_year_docs(user_id),
                'history': self._get_filing_history(user_id),
                'family': self._get_dependents(user_id)
            }
            
            # Add compliance flags
            context['risk_flags'] = self._check_compliance_risks(context)
            
            return context
        except Exception as e:
            logger.error(f"Failed to get tax context: {e}")
            return None
    
    def _get_user_profile(self, user_id):
        """Get core profile data"""
        return db(db.user_profiles.user_id == user_id).select(
            db.user_profiles.filing_status,
            db.user_profiles.spouse_income,
            db.user_profiles.last_agi,
            cache=(cache.ram, 300)  # Cache for 5 minutes
        ).first()
    
    def _get_current_year_docs(self, user_id):
        """Retrieve current tax year documents"""
        current_year = datetime.now().year
        return db(
            (db.tax_documents.user_id == user_id) &
            (db.tax_documents.year == current_year)
        ).select(
            db.tax_documents.doc_type,
            db.tax_documents.issuer,
            db.tax_documents.amount,
            orderby=db.tax_documents.doc_type
        )
    
    def _get_filing_history(self, user_id):
        """Get previous 3 years filing data"""
        return db(db.filing_history.user_id == user_id).select(
            db.filing_history.year,
            db.filing_history.agi,
            db.filing_history.deductions,
            orderby=~db.filing_history.year,
            limitby=(0, self.max_history)
        )
    
    def _get_dependents(self, user_id):
        """Get family/dependent information"""
        return db(db.dependents.user_id == user_id).select(
            db.dependents.name,
            db.dependents.relationship,
            db.dependents.age
        )
    
    def _check_compliance_risks(self, context):
        """Identify potential audit triggers"""
        flags = []
        
        # Large 1099 income check
        for doc in context['documents']:
            if doc.doc_type == '1099-MISC' and doc.amount > 10000:
                flags.append({
                    'type': 'high_1099_income',
                    'message': f"Large 1099-MISC amount (${doc.amount}) may need documentation",
                    'irs_ref': "Pub 535 Ch.6"
                })
        
        # Home office deduction check
        profile = context['profile']
        if profile and 'home_office' in profile.deductions.split(','):
            flags.append({
                'type': 'home_office',
                'message': "Home office deduction requires Form 8829",
                'irs_ref': "Pub 587"
            })
        
        return flags
    
    def log_interaction(self, user_id, question, response, metadata=None):
        """
        Record chatbot interaction for audit trail
        Args:
            user_id: Auth user ID
            question: User's original question
            response: Full AI response
            metadata: Additional context (response time, etc.)
        """
        try:
            db.conversation_log.insert(
                user_id=user_id,
                question=question[:500],
                answer=response.get('answer', '')[:2000],
                sources=json.dumps(response.get('sources', [])),
                risk_flags=json.dumps(response.get('risk_flags', [])),
                response_time=metadata.get('response_time', 0),
                created_on=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Failed to log interaction: {e}")
    
    def format_context_for_ai(self, context):
        """
        Convert database context to LLM-friendly format
        Returns: str
        """
        if not context:
            return "No tax context available"
        
        parts = []
        
        # Profile section
        if context.get('profile'):
            p = context['profile']
            parts.append(
                f"Taxpayer Profile:\n"
                f"- Filing Status: {p.filing_status or 'Not specified'}\n"
                f"- Previous AGI: ${p.last_agi or 0:,.2f}\n"
                f"- Spouse Income: ${p.spouse_income or 0:,.2f}"
            )
        
        # Documents section
        if context.get('documents'):
            docs = "\n".join(
                f"  • {d.doc_type}: ${d.amount:,.2f} ({d.issuer})" 
                for d in context['documents']
            )
            parts.append(f"Current Year Documents:\n{docs}")
        
        # Risk flags
        if context.get('risk_flags'):
            risks = "\n".join(
                f"  ⚠️ {f['message']} (See {f['irs_ref']})"
                for f in context['risk_flags']
            )
            parts.append(f"Compliance Notes:\n{risks}")
        
        return "\n\n".join(parts)

# Initialize for web2py global access
current.tax_ai = TaxAIModel()
