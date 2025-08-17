import os
import logging
from typing import Dict, Any, List
from openai import OpenAI

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ==============================
# Helper functions
# ==============================

def build_context(user_profile: Dict[str, Any], tax_data: Dict[str, Any]) -> str:
    """
    Build a tax-specific context string for the AI model.
    """
    filing_status = user_profile.get("filing_status", "Unknown")
    dependents = user_profile.get("dependents", 0)
    state = user_profile.get("state", "N/A")

    agi = tax_data.get("agi", "N/A")
    w2_income = tax_data.get("w2_income", [])
    prior_returns = tax_data.get("tax_history", [])
    deductions = tax_data.get("deductions", "standard")

    docs_uploaded = tax_data.get("docs", [])

    context = f"""
    User Taxpayer Profile:
    - Filing Status: {filing_status}
    - Dependents: {dependents}
    - State of residence: {state}

    Current Year Tax Data:
    - Adjusted Gross Income (AGI): {agi}
    - W2 Income: {w2_income}
    - Deductions: {deductions}
    - Uploaded Docs: {docs_uploaded}

    Prior Filing History:
    - {prior_returns}

    Knowledge Base (Tax Law Integration):
    - Use IRS 1040 rules for {filing_status} filers.
    - Apply standard deduction unless itemized.
    - Child Tax Credit applies if dependents < 17.
    - Earned Income Tax Credit eligibility depends on AGI, dependents, and filing status.
    - Federal tax brackets (2024): 10%, 12%, 22%, 24%, 32%, 35%, 37%.
    - State-specific rules may apply for {state}.
    """
    return context.strip()


def generate_ai_response(user_question: str, context: str) -> str:
    """
    Generate an AI response using OpenAI GPT with provided tax context.
    """
    try:
        openai_response = client.chat.completions.create(
            model="gpt-4o-mini",  # change to "gpt-4o" for production
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_question}
            ],
            temperature=0.2,  # keep factual
            max_tokens=600
        )
        answer = openai_response.choices[0].message.content.strip()
        return answer

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "⚠️ I couldn’t retrieve an AI response at this time. Please try again later."


# ==============================
# Main Chatbot Logic
# ==============================

class TaxAIChatbot:
    """
    AI Agent for answering user tax questions with context awareness.
    """

    def __init__(self, user_profile: Dict[str, Any], tax_data: Dict[str, Any]):
        self.user_profile = user_profile
        self.tax_data = tax_data
        self.context = build_context(user_profile, tax_data)

    def answer_question(self, question: str) -> str:
        """
        Generate a tax-aware answer to user's question.
        """
        logger.info(f"Received user question: {question}")
        return generate_ai_response(question, self.context)


# ==============================
# Example Usage
# ==============================

if __name__ == "__main__":
    # Example user profile
    user_profile = {
        "name": "John Doe",
        "filing_status": "Married Filing Jointly",
        "dependents": 2,
        "state": "NJ"
    }

    # Example tax data
    tax_data = {
        "agi": 85000,
        "w2_income": [60000, 25000],
        "deductions": "standard",
        "docs": ["W2_2024.pdf", "1099INT.pdf"],
        "tax_history": ["Filed 1040 for 2022, AGI 78000", "Filed 1040 for 2023, AGI 82000"]
    }

    chatbot = TaxAIChatbot(user_profile, tax_data)

    # Example Q&A
    question = "Am I eligible for the Child Tax Credit this year?"
    answer = chatbot.answer_question(question)
    print("Q:", question)
    print("A:", answer)
