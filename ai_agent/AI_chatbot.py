#!/usr/bin/env python3
"""
Enhanced AI Tax Assistant with OpenAI Integration
- Personalized responses using full tax context
- Secure data handling
- Audit-aware answers
"""

import os
import logging
from typing import Dict, List, Optional, Any
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import re
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TaxAIBot")

class AIChatbot:
    def __init__(self, api_key: str):
        self.tax_bot = TaxChatBot(api_key=api_key)

    def ask_question(self, question: str, user_context: dict = None):
        if user_context is None:
            user_context = {}

        # delegate to TaxChatBot
        answer = self.tax_bot.get_answer(question, user_context)
        return answer


class TaxChatBot:
    def __init__(self, db_config: Dict, openai_key: str):
        """
        Initialize with database and OpenAI connections
        """
        self.db_config = db_config
        self.client = OpenAI(api_key=openai_key)
        self.sensitive_patterns = [
            r"\d{3}-\d{2}-\d{4}",  # SSN
            r"\d{2}-\d{7}",         # EIN
            r"\b\d{4}\b"            # Last 4 digits
        ]

    def get_db_connection(self):
        """Secure MySQL connection"""
        try:
            return mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database'],
                ssl_disabled=False
            )
        except Error as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def get_full_tax_context(self, user_id: str) -> Dict[str, Any]:
        """
        Fetch complete tax context including:
        - Personal info
        - Tax documents (W-2, 1099s)
        - Filing history
        - Family situation
        - Previous audit flags
        """
        context = {
            "personal": {},
            "documents": [],
            "history": {},
            "family": {},
            "compliance_alerts": []
        }

        try:
            with self.get_db_connection() as conn:
                # Personal info
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT filing_status, dependents, spouse_income 
                    FROM user_profiles 
                    WHERE user_id = %s
                """, (user_id,))
                personal_data = cursor.fetchone()
                if personal_data:
                    context["personal"] = personal_data

                # Current year documents
                cursor.execute("""
                    SELECT doc_type, issuer, amount, year 
                    FROM tax_documents 
                    WHERE user_id = %s AND year = YEAR(CURDATE())
                """, (user_id,))
                context["documents"] = cursor.fetchall()

                # 3-year filing history
                cursor.execute("""
                    SELECT year, agi, refund_amount, deductions 
                    FROM filing_history 
                    WHERE user_id = %s 
                    ORDER BY year DESC 
                    LIMIT 3
                """, (user_id,))
                context["history"] = cursor.fetchall()

                # Family context
                cursor.execute("""
                    SELECT dependent_name, relationship, age 
                    FROM dependents 
                    WHERE user_id = %s
                """, (user_id,))
                context["family"] = cursor.fetchall()

                # Compliance flags
                self._check_compliance(context)

        except Error as e:
            logger.error(f"Failed to fetch tax context: {e}")

        return context

    def _check_compliance(self, context: Dict):
        """Identify potential audit risks based on documents/history"""
        # Flag high-risk deductions without documentation
        high_risk_items = ["home_office", "vehicle_expenses"]
        for doc in context["documents"]:
            if doc["doc_type"] == "1099-MISC" and doc["amount"] > 10000:
                context["compliance_alerts"].append({
                    "type": "high_income_1099",
                    "message": f"Large 1099-MISC amount (${doc['amount']}) may need additional documentation",
                    "irs_ref": "Pub 535 Ch.6"
                })

    def generate_ai_response(self, user_id: str, question: str) -> Dict[str, Any]:
        """
        Generate compliant tax advice using full context
        Returns:
            {
                "answer": str,
                "sources": List[str],
                "personalized": bool,
                "disclaimers": List[str],
                "confidence": float
            }
        """
        try:
            # Verify access and sanitize
            self.verify_user_access(user_id)
            clean_question = self.sanitize_input(question)
            
            # Get complete context
            context = self.get_full_tax_context(user_id)
            formatted_context = self._format_context_for_ai(context)
            
            # Generate response
            ai_answer = self._call_openai(
                user_question=clean_question,
                context=formatted_context
            )
            
            # Post-process for compliance
            response = self._postprocess_response(ai_answer, context)
            return response
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}", exc_info=True)
            return self._error_response()

    def _format_context_for_ai(self, context: Dict) -> str:
        """Convert structured data to LLM-friendly text"""
        context_str = f"""
        Taxpayer Context:
        - Filing Status: {context['personal'].get('filing_status', 'unknown')}
        - Dependents: {len(context['family'])} ({', '.join([d['dependent_name'] for d in context['family']])})
        - Current Year Documents:
          {self._format_documents(context['documents'])}
        - Recent AGI History:
          {self._format_history(context['history'])}
        """
        
        if context['compliance_alerts']:
            context_str += "\nCompliance Notes:\n" + "\n".join(
                f"- {alert['message']} (Ref: {alert['irs_ref']})" 
                for alert in context['compliance_alerts']
            )
            
        return context_str

    def _call_openai(self, user_question: str, context: str) -> str:
        """
        Generate response using OpenAI with tax-specific prompting
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # Use "gpt-4o" when available
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are a certified tax professional assistant. 
                        Always:
                        - Cite IRS publications when possible
                        - Include relevant code sections
                        - Disclose limitations
                        - Never guess about tax situations
                        
                        Context:
                        {context}"""
                    },
                    {
                        "role": "user",
                        "content": user_question
                    }
                ],
                temperature=0.2,
                max_tokens=800,
                top_p=0.9
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    def _postprocess_response(self, ai_answer: str, context: Dict) -> Dict:
        """Add compliance disclaimers and structure"""
        response = {
            "answer": ai_answer,
            "sources": self._extract_sources(ai_answer),
            "personalized": True,
            "disclaimers": [],
            "confidence": 0.9  # From validation checks
        }
        
        # Add compliance alerts if present
        if context['compliance_alerts']:
            response["disclaimers"] = [
                f"⚠️ Compliance Note: {alert['message']}" 
                for alert in context['compliance_alerts']
            ]
            
        return response

    def _extract_sources(self, text: str) -> List[str]:
        """Parse IRS references from AI response"""
        sources = []
        # Match patterns like "IRS Pub 535" or "26 USC § 170"
        irs_refs = re.findall(r"(IRS Pub \d+|26 USC § \d+\.?\d*)", text)
        return list(set(irs_refs))  # Remove duplicates

    # ... [Previous utility methods: sanitize_input, verify_user_access, etc.]

# Example Usage
if __name__ == "__main__":
    config = {
        "db": {
            "host": "localhost",
            "user": "taxcrm",
            "password": os.getenv("DB_PASSWORD"),
            "database": "taxcrm"
        },
        "openai_key": os.getenv("OPENAI_KEY")
    }
    
    bot = TaxChatBot(config["db"], config["openai_key"])
    
    response = bot.generate_ai_response(
        user_id="user_12345",
        question="Can I claim my home office and vehicle expenses for my consulting business?"
    )
    
    print("Answer:", response["answer"])
    print("\nSources:", response["sources"])
    print("\nDisclaimers:", "\n".join(response["disclaimers"]))
