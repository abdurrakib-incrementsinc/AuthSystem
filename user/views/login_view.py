from django.contrib.auth import login, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers import UserLoginSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from ..models import OTPModel
from utils import helper
from rest_framework_simplejwt.views import TokenObtainPairView
from ..backends import EmailPhoneUsernameAuthenticationBackend as EPUA
from django.conf import settings
from dj_rest_auth.jwt_auth import set_jwt_cookies
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    @staticmethod
    def _direct_login(request, user, serializer):
        """
        Method for login without OTP
        """
        print('direct_login')
        # if settings.REST_SESSION_LOGIN:
        #     login(request, user)
        resp = Response()

        # set_jwt_cookies(
        #     response=resp,
        #     access_token=serializer.validated_data.get(
        #         settings.JWT_AUTH_COOKIE
        #     ),  # noqa
        #     refresh_token=serializer.validated_data.get(
        #         settings.JWT_AUTH_REFRESH_COOKIE
        #     ),
        # )

        # resp.data = serializer.validated_data
        resp.status_code = status.HTTP_200_OK
        resp.data = {
            "detail": "Login successfully",
            "data": serializer.validated_data,
        }
        return resp

    # @staticmethod
    # def _otp_login(user):
    #     """
    #     Method for returning secret key if OTP is active for user
    #     """
    #     print('otp_login')
    #     refresh_token = RefreshToken.for_user(user)
    #     fer_key = helper.encode(str(refresh_token))
    #     return Response(
    #         {"secret": fer_key},
    #         status=status.HTTP_202_ACCEPTED,
    #     )

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        resp = Response()
        try:
            user = EPUA.authenticate(
                request=request,
                username=request.data.get("email"),
                password=request.data.get("password"),
            )
            try:
                otp = generics.get_object_or_404(OTPModel, user=user)
                if otp.is_active:
                    return self._otp_login(user=user)
                return self._direct_login(
                    request=request, user=user, serializer=serializer
                )

            except TokenError as e:
                raise InvalidToken(e.args[0]) from e

        except Exception:
            resp.data = {
                "message": "Username or Password error",
                "data": serializer.validated_data,
            }
            return Response(resp, status=status.HTTP_200_OK)