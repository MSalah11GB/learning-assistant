from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.dummy.echo")
def echo_task() -> dict[str, str]:
    return {"status": "ok", "task": "echo_task"}
