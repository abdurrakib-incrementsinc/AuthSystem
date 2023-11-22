from rest_framework import serializers
from ..models import Branch, Floor, Table
from user.models import User


class BranchManagerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user_information.first_name', read_only=True)
    last_name = serializers.CharField(source='user_information.last_name', read_only=True)
    profile_pic = serializers.ImageField(source='user_information.profile_pic', read_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'profile_pic')


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"
        read_only_fields = ('slug',)


class FloorSerializer(serializers.ModelSerializer):
    tables = TableSerializer(source='floor_table', many=True, read_only=True)
    total_capacity = serializers.CharField(read_only=True)
    total_table = serializers.CharField(read_only=True)

    class Meta:
        model = Floor
        fields = "__all__"
        read_only_fields = ('slug', 'branch', 'tables')


class BranchSerializer(serializers.ModelSerializer):
    manager = BranchManagerSerializer(read_only=True)
    floor = FloorSerializer(source='branch_floor', many=True, read_only=True)

    class Meta:
        model = Branch
        fields = "__all__"
        read_only_fields = ('slug', 'manager', 'qr_image')

