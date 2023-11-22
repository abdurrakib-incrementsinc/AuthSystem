import json
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from ..models import User
from utils import helper


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        style={'input_type': 'password'}
    )
    def validate(self, data):
        token = self.context.get("token")
        user = self.__validate_user_token(token)
        if data["new_password"] != data["new_password_confirm"]:
            raise serializers.ValidationError("Passwords do not match.")
        user.set_password(data["new_password"])
        user.save()
        return data

    def __validate_user_token(self, token):
        _decrypted_data = helper.decode(token)

        _decrypted_data_dict = json.loads(_decrypted_data.replace("'", '"'))

        token = _decrypted_data_dict["token"]

        encoded_pk = _decrypted_data_dict["enc_pk"]

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")
        return user