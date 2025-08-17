# TaxCRM API

A lightweight CRM + Tax Processing API (FastAPI).

## Features
- FastAPI backend
- Secure S3 presigned uploads
- Simple 1040 calculator
- Agent tool stubs (intake, e-sign)
- Logging + Audit trail

## Setup
```bash
git clone https://github.com/zjerryxie/TaxCRM.git
cd TaxCRM/api
pip install -r requirements.txt
uvicorn main:app --reload
