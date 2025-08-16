from langchain.agents import Tool, initialize_agent
from app.services import document_ai, risk_analysis

tools = [
    Tool(
        name="W-2 Parser",
        func=document_ai.extract_w2_data,
        description="Extract wages, taxes from W-2s"
    ),
    Tool(
        name="Audit Risk Predictor",
        func=risk_analysis.audit_risk_score,
        description="Predict IRS audit probability (0-1)"
    )
]

tax_agent = initialize_agent(
    tools,
    llm=OpenAI(temperature=0),
    agent="zero-shot-react-description"
)

def query_agent(prompt: str) -> str:
    """Unified AI interface for all tax tasks"""
    return tax_agent.run(prompt)
