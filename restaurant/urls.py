from rest_framework import routers
from restaurant.views import RestaurantViewSet, BranchViewSets, FloorViewSets, TableViewSets
from django.urls import path

router = routers.DefaultRouter()
router.register('restaurant', RestaurantViewSet, basename='restaurant')
router.register('branch', BranchViewSets, basename='branch')
router.register('floor', FloorViewSets, basename='floor')
router.register('table', TableViewSets, basename='table')

urlpatterns = [

] + router.urls
