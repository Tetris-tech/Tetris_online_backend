start: uvicorn src.main:app --host 127.0.0.1 --port 8000
celery_beat: celery --app src.config.celery.app beat --loglevel info
celery_worker: celery --app src.config.celery.app worker --loglevel info
migrations: alembic upgrade head
