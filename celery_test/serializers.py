from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
