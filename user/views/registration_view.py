import json
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.registration_serializer import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from ..models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from utils import helper


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if new_user := serializer.save():
            host = request.META
            http_host = host['HTTP_HOST']
            http_ref = host.get('HTTP_ORIGIN', '127.0.0.1:800')
            # to verify the user
            if self._user_validation_token(user, new_user.email, http_host, http_ref):
                token = get_tokens_for_user(new_user) # generate token for user
                return Response(
                    {'token': token, 'user': serializer.data, 'msg': 'Check Mail to Verify The Account'},
                    status=status.HTTP_201_CREATED
                )
        return Response({"details": "Account Creation Failed"}, status=status.HTTP_400_BAD_REQUEST)

    def verify_user(self, request, *args, **kwargs):  # to verify the user
        token = self.request.query_params.get('token', None)  # get the token from query params
        user, key, ref = self._validate_user(token)
        if user or key:
            user.is_active = True
            user.save()
            return Response({'msg': 'User Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response({'details': 'User Verification Failed'}, status=status.HTTP_400_BAD_REQUEST)

    def _user_validation_token(self, user_model, email=None, http_host=None, http_ref=None):
        user = User.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(user)
        # creating string that is safe to be included in urls
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        to_enc = {'token': token, 'enc_pk': encoded_pk, 'ref': http_ref}
        enc_token = helper.encode(str(to_enc))
        # Send the one-time password to the user's email or phone number
        if self.__send_verification_mail(user, str(enc_token, "UTF-8"), http_host):
            return True
        # if activation mail send failed delete user
        user.delete()
        return Response({"message": "Verification Mail Send Failed"}, status=status.HTTP_400_BAD_REQUEST,)

    def __send_verification_mail(self, user, obj, http_host=None):
        try:
            protocol = "http"
            protocol = "http://" if protocol not in http_host else ""
            url = f"{protocol}{http_host}/user/verify-user/?token={obj}"
            html_message = render_to_string(
                "activation_email.html",
                context={"url": url},
            )
            plain_message = strip_tags(html_message)

            message = EmailMultiAlternatives(
                subject="Email Confirmation",
                body=plain_message,
                from_email=None,
                to=[user.email],
            )

            message.attach_alternative(html_message, "text/html")
            message.send()
            return True
        except Exception:
            return False

    def _validate_user(self, token):
        _decrypted_data = helper.decode(str(token))
        _decrypted_data_dict = json.loads(_decrypted_data.replace("'", '"'))

        token = _decrypted_data_dict['token']
        encoded_pk = _decrypted_data_dict['enc_pk']
        ref = _decrypted_data_dict['ref']

        if token is None or encoded_pk is None:
            return Response({'details': "Missing Value"}, status=status.HTTP_400_BAD_REQUEST)

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return None, None, ref
        return user, _decrypted_data_dict, ref

