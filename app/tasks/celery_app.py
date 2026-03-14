from celery import Celery

from app.core.config import settings

celery_app = Celery("pegasus_ops", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.task_routes = {
    "app.tasks.media_tasks.*": {"queue": "media"},
}
