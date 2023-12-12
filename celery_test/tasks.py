from celery import shared_task
import time
from .models import Task
from django.db import connection


@shared_task(bind=True)
def task_example(self, message):
    # stop the execution for 5 seconds
    time.sleep(10)
    for i in range(3):
        print(i)
    task = Task.objects.create(name=message)
    task.save()
    return f"Task completed: {message}"


