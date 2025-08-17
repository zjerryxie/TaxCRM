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
