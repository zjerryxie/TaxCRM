from fastapi import APIRouter
from app.services import risk_analysis, document_ai

router = APIRouter()

@router.post("/ai/check-deadline")
async def check_deadline(client_id: int):
    client = get_client(client_id)
    return { "is_late": risk_analysis.check_deadlines(client) }

@router.post("/ai/process-w2")
async def process_w2(s3_path: str):
    return document_ai.extract_w2_data(s3_path)  # Or use Celery: process_w2_async.delay(s3_path)
