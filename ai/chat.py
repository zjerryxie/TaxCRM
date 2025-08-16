from langchain.llms import OpenAI

def generate_response(client_query: str) -> str:
    llm = OpenAI(model="gpt-4", api_key=os.getenv('OPENAI_KEY'))
    prompt = f"""
    As a tax CRM assistant, respond professionally to a client asking:
    '{client_query}'. 
    Use their tax data (filing status: {client.filing_status}, year: {client.tax_year}).
    """
    return llm(prompt)
