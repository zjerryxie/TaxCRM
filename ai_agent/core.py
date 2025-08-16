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

from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history")
tax_agent = initialize_agent(
    tools, 
    llm=OpenAI(temperature=0), 
    memory=memory,  # <- Critical for agent behavior
    agent="conversational-react-description"  # Changed agent type
)

def query_agent(prompt: str) -> str:
    """Unified AI interface for all tax tasks"""
    return tax_agent.run(prompt)

tools.append(
    Tool(
        name="IRS Rule Lookup",
        func=lambda q: get_irs_rule(current_year, q),
        description="Fetch latest IRS rules for forms (1040, 1120, etc.)"
    )
)
