from celery import Celery

app = Celery(
    "tasks",
    broker="pyamqp://guest@localhost//",  # Use the AMQP broker (RabbitMQ)
    backend="cache+memory://"
)

@app.task
def count_users_task():
    user_count = 0  # Simulated user count
    # In a real-world scenario, you would perform the actual user counting logic here
    user_count += 1
    return user_count
