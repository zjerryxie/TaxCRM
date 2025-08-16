def get_agent_prompt(client: Client):
    base = "You're a tax assistant for {filing_status} filers."
    if client.income > 1e6:
        base += " Focus on AMT and estate planning."
    return base
