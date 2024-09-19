from celery import Celery

from .settings import Settings

BROKER_URL = "redis://{}:{}/0".format(
    Settings.REDIS_HOST.value,
    Settings.REDIS_PORT.value,
)

app = Celery(__name__)
app.conf.broker_url = BROKER_URL,
app.conf.result_backend = BROKER_URL

app.conf.beat_schedule = {}
