import requests

def get_irs_rule(tax_year: int, form: str) -> dict:
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
