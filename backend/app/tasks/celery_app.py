from celery import Celery

from app.core.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "learning_assistant",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.dummy"],
)

celery_app.conf.update(
    task_default_queue="learning_assistant",
    task_track_started=True,
    timezone="UTC",
    enable_utc=True,
)
