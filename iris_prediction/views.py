from rest_framework.views import APIView
from .serializers import IrisSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from joblib import load
model = load('./SavedModels/model.joblib')
# Create your views here.


class IrisView(APIView):
    @extend_schema(request=IrisSerializer)
    def post(self, request, *args, **kwargs):
        serializer = IrisSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sepal_length = serializer.validated_data.get('sepal_length')
        sepal_width = serializer.validated_data.get('sepal_width')
        petal_length = serializer.validated_data.get('petal_length')
        petal_width = serializer.validated_data.get('petal_width')
        y_pred = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
        if y_pred[0] == 0:
            name = 'Setosa'
        elif y_pred[0] == 1:
            name = 'Verscicolor'
        else:
            name = 'Virginica'
        return Response({'Class': name, 'Prediction': y_pred[0]}, status=status.HTTP_200_OK)