from rest_framework import serializers


class IrisSerializer(serializers.Serializer):
    sepal_length = serializers.IntegerField()
    sepal_width = serializers.IntegerField()
    petal_length = serializers.IntegerField()
    petal_width = serializers.IntegerField()
