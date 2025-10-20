from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    # The list of files where Celery looks for tasks
    include=[
        'app.agents.validation_agent',
        'app.agents.qa_agent',
    ]
)
celery_app.conf.timezone = 'UTC'