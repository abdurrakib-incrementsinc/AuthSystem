from rest_framework import viewsets
from ..serializers.restaurant_serializer import RestaurantSerializer
from ..models import Restaurant
from django.contrib.auth import get_user_model
User = get_user_model()


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(owner=self.request.user)
