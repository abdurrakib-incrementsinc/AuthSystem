from django.shortcuts import render
from rest_framework.decorators import api_view
from .tasks import task_example
from rest_framework.response import Response
from rest_framework import status
import time
# Create your views here.


@api_view(['POST'])
def execute_celery(request):
    # get the message from post request
    message = request.data.get('message', 'Hello! Everyone')
    # trigger the celery task
    task_example.delay(message)
    print('executed')

    # response after successfully calling the celery task
    return Response(
        {'status': "Get the response without the 15 seconds delay."},
        status=status.HTTP_200_OK
    )


