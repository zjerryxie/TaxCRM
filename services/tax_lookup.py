import requests

def get_irs_rule(tax_year: int, form: str) -> dict:
    url = f"https://api.irs.gov/pub/irs-drop/rp-{tax_year}-{form}.json"
    response = requests.get(url, headers={"Accept": "application/json"})
    return response.json()  # Returns latest IRS rules for form
