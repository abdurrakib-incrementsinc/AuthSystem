import json
from django.contrib.auth import login, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.reset_passsword_serializer import EmailSerializer, PasswordResetSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from ..models import User, OTPModel
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from utils import helper
from utils.email_sender import templated_email_send
from django.shortcuts import redirect
# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class PasswordResetView(generics.GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        UserModel = get_user_model()
        try:
            return self.__user_validate_and_send_token(UserModel, email)
        except UserModel.DoesNotExist:
            return Response(
                {"message": "User not found with this email"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def __user_validate_and_send_token(self, UserModel, email):
        user = UserModel.objects.get(email=email)
        # protocol
        http_host = self.request.META.get('HTTP_HOST')
        http_ref = self.request.META.get('HTTP_ORIGIN', '127.0.0.1:8000')
        # encryption
        token = PasswordResetTokenGenerator().make_token(user)
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        to_enc = {'token':token, 'enc_pk': encoded_pk, 'ref': http_ref}
        enc_token = helper.encode(str(to_enc))
        enc_token = str(enc_token, 'utf-8')

        protocol = "http://" if "http" not in http_host else ""
        url = f"{protocol}{http_host}/user/password-verify/?token={enc_token}"
        try:
            username = (user.user_information.first_name + user.user_information.last_name)
        except Exception:
            username = "Dear"
        templated_email_send(
            subject="Reset Password",
            send_to=[user.email],
            context={'reset_link': url, 'user_name': username},
            template="reset_email.html",
        )
        return Response({"message": "Mail Send"}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(viewsets.ModelViewSet):
    serializer_class = PasswordResetSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = PasswordResetSerializer(
            data=request.data, context={"token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Password changed"})

    def verify_token(self, request, *args, **kwargs):
        token = self.request.query_params.get("token", None)

        # validate token
        user, key, ref = self._validate_user(token)
        if user or key:
            return redirect(to=f"{ref}/reset-password/{token}")
        return redirect(to=f"{ref}/")

    def _validate_user(self, token):
        """
        Verify token and encoded_pk and then set new password.
        """
        # decode token
        _decrypted_data = helper.decode(str(token))
        # replace all single quote with double quote
        _decrypted_data_dict = json.loads(_decrypted_data.replace("'", '"'))

        # print(_decrypted_data)
        token = _decrypted_data_dict["token"]
        encoded_pk = _decrypted_data_dict["enc_pk"]
        ref = _decrypted_data_dict["ref"]

        if token is None or encoded_pk is None:
            return Response(
                {"detail": "Missing value"}, status=status.HTTP_400_BAD_REQUEST
            )

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return None, None, ref
        return user, _decrypted_data_dict, ref
