from rest_framework import viewsets
from ..serializers.restaurant_serializer import RestaurantSerializer
from ..models import Restaurant
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
User = get_user_model()


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.request.query_params.get('search', None)
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Restaurant.objects.none()
        if user.is_superuser:
            return self.queryset
        if user.is_owner:
            return Restaurant.objects.filter(owner=user)
        if slug:
            return get_object_or_404(Restaurant, slug=slug)

    def perform_create(self, serializer):
        user = self.request.user
        user.is_owner = True
        user.save()
        serializer.save(owner=self.request.user)
