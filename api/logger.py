import logging

logger = logging.getLogger("taxcrm")
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def log_audit(func):
    """Decorator to log audit info for compliance"""
    async def wrapper(*args, **kwargs):
        logger.info(f"Audit: {func.__name__} called with args={args}, kwargs={kwargs}")
        return await func(*args, **kwargs)
    return wrapper
