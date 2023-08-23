from fastapi import FastAPI
from celery import Celery
from celery.schedules import crontab
from celery.result import AsyncResult
from .app import count_users_task

app = FastAPI()

# Configure Celery
celery = Celery(__name__)
celery.config_from_object("celery_app")

# Schedule the task to run every day at midnight
celery.conf.beat_schedule = {
    "count-users-task": {
        "task": "main.count_users_task",
        "schedule": crontab(minute=0, hour=0),  # Midnight
    },
}

@app.get("/count_users")
async def count_users():
    async_result = count_users_task.delay()
    return {"task_id": async_result.id}

@app.get("/check_task_status/{task_id}")
async def check_task_status(task_id: str):
    async_result = AsyncResult(task_id, app=celery)
    return {"task_status": async_result.status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
