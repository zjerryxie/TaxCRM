from models import IntakeRequest, TaxReturnResponse
from calc1040 import calc_1040

def run_1040(request: IntakeRequest) -> TaxReturnResponse:
    result = calc_1040(request.income, request.filing_status)
    return TaxReturnResponse(
        client_name=f"{request.first_name} {request.last_name}",
        agi=result["agi"],
        taxable_income=result["taxable_income"],
        tax_liability=result["tax_liability"],
        refund=result["refund"]
    )
