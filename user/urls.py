from django.urls import path
from user.views import (
    ChangePasswordView,
    UserRegistrationView,
    PasswordResetView,
    PasswordResetConfirmView,
    UserLoginView
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path('register/', UserRegistrationView.as_view({'post': 'create'}), name="register"),
    path('verify-user/', UserRegistrationView.as_view({'get': 'verify_user'}), name="verify_user"),
    path('password-reset/', PasswordResetView.as_view(), name="password_reset"),
    path("password-verify/", PasswordResetConfirmView.as_view({"get": "verify_token"}), name="password-verify"),
    path("password-conform/<str:token>/", PasswordResetConfirmView.as_view({"post": "post"}), name="reset-password"),
    path('resend-email/', UserRegistrationView.as_view({'get': 'resend_verification_email'}), name="resend_email"),
    path('change-password/', ChangePasswordView.as_view(), name="change_password"),
]
