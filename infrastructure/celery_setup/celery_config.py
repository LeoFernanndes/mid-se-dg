import logging
import os

from celery import Celery
from dotenv import load_dotenv


load_dotenv()


redis_host = os.environ.get("REDIS_HOST", "redis")
redis_port = os.environ.get("REDIS_PORT", 6379)

celery_app = Celery(
    'celery-dg',
    broker=f'redis://{redis_host}:{redis_port}/0',
    backend=f'redis://{redis_host}:{redis_port}/1',
    include=["infrastructure.celery_setup.celery_tasks"]
)

celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_routes={
        'infrastructure.celery_setup.celery_tasks.*': {'queue': 'default'},
    },
    beat_schedule={
        'run-every-1-second': {
            'task': 'celery_tasks.periodic',
            'schedule': 2.0,
        },
    }
)

celery_app.conf.timezone = 'UTC'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
