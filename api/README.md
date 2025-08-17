# TaxCRM API

Starter FastAPI service with:
- Intake flow
- S3 presigned doc upload/download
- Simplified 1040 calculator
- E-sign stub (DocuSign/HelloSign ready)

## Run Locally
```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
