from pydantic import BaseModel
from typing import Optional

class IntakeRequest(BaseModel):
    first_name: str
    last_name: str
    ssn: str
    income: float
    filing_status: str = "single"  # single, married, etc.

class TaxReturnResponse(BaseModel):
    client_name: str
    agi: float
    taxable_income: float
    tax_liability: float
    refund: float

class PresignRequest(BaseModel):
    filename: str
    operation: str  # "upload" or "download"

class PresignResponse(BaseModel):
    url: str
