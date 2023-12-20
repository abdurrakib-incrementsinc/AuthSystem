import socketio
import json
import jwt
from chatapi.models import Conversation, Message
from django.contrib.auth import get_user_model
from django.conf import settings
from asgiref.sync import sync_to_async
from django.db.models import Q
from socketio import AsyncServer, AsyncRedisManager
User = get_user_model()


class SocketHandler:
    def __init__(self):
        self.mgr = AsyncRedisManager('redis://localhost:6379')
        self.sio = AsyncServer(
            async_mode="asgi", client_manager=self.mgr, cors_allowed_origins="*"
        )

    async def connect(self, sid, env):
        query_params = env.get('QUERY_STRING')
        params = dict(param.split("=") for param in query_params.split("&"))
        receiver_id = params.get('id', '')
        print(receiver_id)

        self.receiver = await sync_to_async(User.objects.get)(pk=receiver_id)
        print(self.receiver)

        headers = env.get("asgi.scope").get('headers', [])
        for key, value in headers:
            if key.decode('utf-8') == 'authorization':
                token = value.decode('utf-8').split()[1]
                self.user = await sync_to_async(self.get_user_from_token)(token)
                print(self.user)

        conv = await sync_to_async(
            lambda: Conversation.objects.filter(
                Q(user_one=self.user, user_two=self.receiver)
                | Q(user_one=self.receiver, user_two=self.user)
                ).first()
        )()
        if not conv:
            conv = await sync_to_async(Conversation.objects.create)(
                user_one=self.user,
                user_two=self.receiver,
            )
            await sync_to_async(conv.save)()
        self.chat_room = str(conv.name)
        print("SocketIO connect")
        await self.sio.enter_room(sid, self.chat_room)
        await self.sio.emit("connect", f"Connected as {sid}")

    async def print_message(self, sid, data):
        print("Socket ID", sid)
        conv = await sync_to_async(Conversation.objects.get)(name=self.chat_room)
        message = await sync_to_async(Message.objects.create)(
            conversation=conv,
            content=data,
            sender=self.user,
            receiver=self.receiver
        )
        await sync_to_async(message.save)()
        await self.sio.emit("new_message", data, room=self.chat_room)

    async def disconnect(self, sid):
        print("SocketIO disconnect")

    def get_user_from_token(self, token):
        try:
            user_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return User.objects.get(pk=user_data['user_id'])
        except jwt.ExpiredSignatureError:
            # Handle token expiration
            print("Token has expired.")
        except jwt.InvalidTokenError:
            # Handle invalid token
            print("Invalid token.")
        except User.DoesNotExist:
            # Handle user not found
            print("User not found.")


# Create an instance of the SocketIOHandler
socket_handler = SocketHandler()

# Register the event handlers
socket_handler.sio.on("connect")(socket_handler.connect)
socket_handler.sio.on("message")(socket_handler.print_message)
socket_handler.siot.on("disconnect")(socket_handler.disconnect)