from django.shortcuts import render
from rest_framework.decorators import api_view
from .tasks import task_example
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
from drf_spectacular.utils import extend_schema
import time
# Create your views here.


@extend_schema(request=TaskSerializer)
@api_view(['POST'])
def execute_celery(request):
    # get the message from post request
    serializer = TaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = serializer.validated_data.get('name')
    print(message)
    # trigger the celery task
    task_example.delay(message)

    # response after successfully calling the celery task
    return Response(
        {'status': "Get the response without the 15 seconds delay."},
        status=status.HTTP_200_OK
    )


