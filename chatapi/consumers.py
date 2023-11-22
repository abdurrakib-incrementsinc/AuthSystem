import json

import jwt
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Q

from .models import Conversation, Message
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings


class ChatWebSocketConsumer(WebsocketConsumer):
    def connect(self):
        self.receiver_id = self.scope['url_route']['kwargs']['id']
        self.receiver = User.objects.get(id=self.receiver_id)
        headers = self.scope.get('headers', [])
        for key, value in headers:
            if key.decode('utf-8') == 'authorization':
                token = value.decode('utf-8').split()[1]
                self.user = self.get_user_from_token(token)
                print(self.user)
        conv = Conversation.objects.filter(
            Q(user_one=self.user, user_two=self.receiver)
            | Q(user_one=self.receiver, user_two=self.user)
        ).first()
        if not conv:
            conv = Conversation.objects.create(
                user_one=self.user,
                user_two=self.receiver,
            )
            conv.save()
        self.group_name = str(conv.name)
        print(self.group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        print("text_data..", text_data)
        conv = Conversation.objects.get(name=self.group_name)
        message = Message.objects.create(
            conversation=conv,
            content=text_data,
            sender=self.user,
            receiver=self.receiver
        )
        message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat.message',  # event
                'message': text_data
            }
        )

    def chat_message(self, event):
        msg = event['message']
        self.send(msg)

    def disconnect(self, code):
        self.close()

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