from django.urls import path
from .views import execute_celery


urlpatterns = [
    path('celery-execute/', execute_celery, name="celery_task")
]
