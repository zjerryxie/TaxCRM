import requests
from pydantic import conint, constr

def get_irs_rule(tax_year: conint(ge=2020, le=2025), form: constr(regex=r'^(1040|1120)$')): 
    try:
        response = requests.get(
            f"https://api.irs.gov/pub/irs-drop/rp-{tax_year}-{form}.json",
            timeout=10
        )
        response.raise_for_status()  # Raise HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"IRS API failed: {e}")
        return {"error": "IRS service unavailable"}
