import socketio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


class ChatSocketIo:
    def __init__(self):
        self.group_name = "rakib"
        self.sio = sio

    async def on_connect(self, sid, environ):
        await self.sio.emit('connected', room=sid)
        await self.sio.enter_room(sid, self.group_name)

    async def on_message(self, sid, data):
        await self.sio.emit('chat.message', data, room=self.group_name)

    async def on_disconnect(self, sid):
        await self.sio.leave_room(sid, self.group_name)