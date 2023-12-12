from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from user.serializers import PasswordChangeSerializer
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework import status


class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['new_password']
        user.set_password(password)
        user.save()
        if settings.LOGOUT_ON_PASSWORD_CHANGE:
            logout(request)
            return redirect('/')
        return Response({'success': 'Password changed successfully'})

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
