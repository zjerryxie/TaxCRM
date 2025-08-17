from models import IntakeRequest, TaxReturnResponse
from calc1040 import calc_1040

def process_intake(request: IntakeRequest) -> TaxReturnResponse:
    calc = calc_1040(request.income, request.filing_status)
    return TaxReturnResponse(
        client_name=f"{request.first_name} {request.last_name}",
        agi=calc["agi"],
        taxable_income=calc["taxable_income"],
        tax_liability=calc["tax_liability"],
        refund=calc["refund"]
    )

"""
Client intake tool stub
Future: process onboarding forms, validate identity (KYC), 
and push structured data into CRM DB.
"""

def intake_new_client(client_data: dict) -> dict:
    # TODO: Add AI pipeline (OCR, doc validation, auto-form fill)
    return {"status": "success", "client": client_data}
