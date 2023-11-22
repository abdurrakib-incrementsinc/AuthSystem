from django.urls import path
from .views import registration_view, reset_password_view, login_view
from user import views
urlpatterns = [
    path("login/", login_view.UserLoginView.as_view(), name="login"),
    path('register/', registration_view.UserRegistrationView.as_view({'post': 'create'}), name="register"),
    path('verify-user/', registration_view.UserRegistrationView.as_view({'get': 'verify_user'}), name="verify_user"),
    path('password-reset/', reset_password_view.PasswordResetView.as_view(), name="password_reset"),
    path("password-verify/", reset_password_view.PasswordResetConfirmView.as_view({"get": "verify_token"}), name="password-verify"),
    path("password-confirm/<str:token>/", reset_password_view.PasswordResetConfirmView.as_view({"post": "post"}), name="reset-password"),
]
