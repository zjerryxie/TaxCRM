# app/tasks/async_tasks.py
from celery import Celery
from app.services.document_ai import extract_w2_data

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def process_w2_async(s3_path: str):
    return extract_w2_data(s3_path)
