from fastapi import APIRouter
from app.services import risk_analysis, document_ai

router = APIRouter()

from sse_starlette.sse import EventSourceResponse

@router.get("/ai/stream")
async def ai_stream(request: Request):
    async def event_generator():
        while True:
            yield {"data": get_ai_update()}
            await asyncio.sleep(1)
    return EventSourceResponse(event_generator())
    
@router.post("/ai/check-deadline")
async def check_deadline(client_id: int):
    client = get_client(client_id)
    return { "is_late": risk_analysis.check_deadlines(client) }

@router.post("/ai/process-w2")
async def process_w2(s3_path: str):
    return document_ai.extract_w2_data(s3_path)  # Or use Celery: process_w2_async.delay(s3_path)

from fastapi import APIRouter
from app.services.vector_db import init_vector_store
from langchain.chains import RetrievalQA

router = APIRouter()

@router.post("/ai/chat")
async def tax_qa(question: str):
    vector_store = init_vector_store(get_all_clients())  # Implement get_all_clients()
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(model="gpt-4"),
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    return qa.run(question)
