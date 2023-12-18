from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

import socketio
import eventlet

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

class ChatWebSocketConsumer:
    def __init__(self):
        self.group_name = "rakib"
        self.sio = sio

    @sio.event
    async def connect(self, sid, environ):
        await self.sio.emit('connected', room=sid)
        await self.sio.enter_room(sid, self.group_name)

    @sio.event
    async def message(self, sid, data):
        await self.sio.emit('chat.message', data, room=self.group_name)

    @sio.event
    async def disconnect(self, sid):
        await self.sio.leave_room(sid, self.group_name)

# Decorate your views with csrf_exempt and require_GET
@csrf_exempt
@require_GET
def socketio_view(request):
    # Start the application
    consumer = ChatWebSocketConsumer()

    # Serve the socket.io app using eventlet
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 8000)), app)

    return HttpResponse("WebSocket server running...")