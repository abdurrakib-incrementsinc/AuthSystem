from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True,
        validators=[validate_password]
    )
    new_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True,
        validators=[validate_password]
    )
    conform_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True,
        validators=[validate_password]
    )

    def validate(self, attrs):
        user = self.context['request'].user
        if user.check_password(attrs['old_password']):
            if attrs['new_password'] != attrs['conform_password']:
                raise serializers.ValidationError({'Error': "The password doesn't match"})
            return attrs
        raise serializers.ValidationError({'Error': "Old password is incorrect"})
