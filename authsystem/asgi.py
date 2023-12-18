# # """
# # ASGI config for authsystem project.
# #
# # It exposes the ASGI callable as a module-level variable named ``application``.
# #
# # For more information on this file, see
# # https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
# # """
# #
# # import os
# #
# # from django.core.asgi import get_asgi_application
# # from channels.routing import ProtocolTypeRouter, URLRouter
# # from django.urls import path
# # from channels.security.websocket import AllowedHostsOriginValidator
# # from chatapi.consumers import ChatWebSocketConsumer
# #
# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authsystem.settings')
# #
# # # Initialize Django ASGI application early to ensure the AppRegistry
# # # is populated before importing code that may import ORM models.
# # django_asgi_app = get_asgi_application()
# #
# # application = ProtocolTypeRouter({
# #     "http": django_asgi_app,
# #     "websocket": AllowedHostsOriginValidator(
# #         URLRouter([
# #             path('ws/gn/sc/<str:id>/', ChatWebSocketConsumer.as_asgi())
# #         ])
# #     )
# # })
#
# import os
# from django.core.asgi import get_asgi_application
# from websocket_connect.consumers import websocket_applciation
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authsystem.settings')
#
# django_application = get_asgi_application()
#
#
# async def application(scope, receive, send):
#     if scope['type'] == 'http':
#         await django_application(scope, receive, send)
#     elif scope['type'] == 'websocket':
#         await websocket_applciation(scope, receive, send)
#     else:
#         raise NotImplementedError(f"Unknown scope type {scope['type']}")


import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authsystem.settings')
django_asgi_app = get_asgi_application()


# it's important to make all other imports below this comment
import socketio
from socket_io.sockets import sio


application = socketio.ASGIApp(sio, django_asgi_app)