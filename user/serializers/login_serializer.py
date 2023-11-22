from rest_framework import serializers
from ..models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserLoginSerializer(TokenObtainPairSerializer):
    """
        JWT Custom Token Claims Serializer
        """

    new_restaurant = serializers.BooleanField(
        source="new_restaurant_check", read_only=True
    )

    @staticmethod
    def validate_email_verification_status(user):
        from allauth.account import app_settings

        if (
            app_settings.EMAIL_VERIFICATION
            == app_settings.EmailVerificationMethod.MANDATORY
            and not user.emailaddress_set.filter(
                email=user.email, verified=True
            ).exists()
        ):
            raise serializers.ValidationError(_("E-mail is not verified."))

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        cls.validate_email_verification_status(user)
        # Add custom claims
        token["email"] = user.email
        token["is_superuser"] = user.is_superuser
        token["is_staff"] = user.is_staff

        # token["new_category"] = user.new_restaurant_check
        # token["new_items"] = user.item_check
        # token["new_menus"] = user.menu_check
        try:
            token["branch"] = user.branch_slug
        except Exception:
            token["branch"] = ""
        return token

    class Meta:
        model = User
        fields = "__all__"