# app/tasks/async_tasks.py
from celery import Celery
from app.services.document_ai import extract_w2_data

celery = Celery('tasks', broker='redis://localhost:6379/0')

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

@celery.task(bind=True)
def process_w2_async(self, s3_path: str):
    try:
        from app.services.document_ai import extract_w2_data
        return extract_w2_data(s3_path)
    except Exception as e:
        logger.error(f"Failed to process W-2: {e}")
        self.retry(exc=e, countdown=60)  # Retry after 60 seconds
