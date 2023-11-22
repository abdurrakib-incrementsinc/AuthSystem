import random
import re

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from ..models import User, UserInformation
from rest_framework import validators
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            validators.UniqueValidator(queryset=User.objects.all())
        ]
    )
    password1 = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True,
        validators=[validate_password],
    )

    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise validators.ValidationError({'password1':'password does not match'})
        return attrs

    def create_username(self, email):
        if email is None:
            return None
        username = email.split('@')[0]
        username = re.sub(r'[._-]', '', username)
        username = username.lower()
        if username == '':
            return None

        while User.objects.filter(username=username).exists():
            username += str(random.randint(1, 1000))
        return username

    def create(self, validated_data):
        username = self.create_username(validated_data["email"])
        user = User.objects.create(
            email=validated_data['email'],
            username=username
        )
        user.set_password(validated_data['password1'])
        user.save()
        userinfo = UserInformation.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        userinfo.save()
        return user
