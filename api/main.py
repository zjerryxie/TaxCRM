from fastapi import FastAPI, UploadFile, HTTPException
from tools import intake, docs, calculator, esign
from models import IntakeRequest, TaxReturnResponse, PresignRequest, PresignResponse

app = FastAPI(title="TaxCRM API", version="0.1")

@app.post("/intake", response_model=TaxReturnResponse)
async def intake_client(request: IntakeRequest):
    return intake.process_intake(request)

@app.post("/docs/presign", response_model=PresignResponse)
async def get_presign_url(req: PresignRequest):
    url = docs.generate_presign_url(req.filename, req.operation)
    if not url:
        raise HTTPException(status_code=500, detail="Failed to generate presign URL")
    return PresignResponse(url=url)

@app.post("/return/calculate", response_model=TaxReturnResponse)
async def calculate_return(request: IntakeRequest):
    return calculator.run_1040(request)

@app.post("/esign")
async def esign_return(request: IntakeRequest):
    return esign.send_for_esign(request)
