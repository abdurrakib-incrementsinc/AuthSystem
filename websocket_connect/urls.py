from django.urls import path
from .views import socketio_view

urlpatterns = [
    path('socketio/', socketio_view, name='socketio_view'),
]
