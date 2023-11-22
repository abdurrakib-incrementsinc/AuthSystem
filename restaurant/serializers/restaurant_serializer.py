from rest_framework import serializers
from ..models import Restaurant, Branch
from restaurant.serializers import BranchSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(source='restaurant_branch', many=True, read_only=True)
    branch_name = serializers.CharField(max_length=120, write_only=True)
    manager_email = serializers.EmailField(write_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ['branches', 'slug', 'owner']

    def create(self, validated_data):
        branch_name = validated_data.pop('branch_name', None)
        manager_email = validated_data.pop('manager_email', None)
        restaurant = super(RestaurantSerializer, self).create(validated_data)
        branch = Branch.objects.create(
            restaurant=restaurant,
            name=branch_name,
            email=manager_email,
            manager=self.context.get('request').user,
        )
        branch.save()
        return restaurant
