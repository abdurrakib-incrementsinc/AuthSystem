from django.urls import path
from .views import IrisView

urlpatterns = [
    path('iris/', IrisView.as_view(), name='iris')
]

