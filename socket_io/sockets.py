import socketio
import json

mgr = socketio.AsyncRedisManager('redis://localhost:6379')
sio = socketio.AsyncServer(
    async_mode="asgi", client_manager=mgr, cors_allowed_origins="*"
)


# establishes a connection with the client
@sio.on("connect")
async def connect(sid, env):
    chat_id = "bd"
    print("SocketIO connect")
    await sio.enter_room(sid, chat_id)
    await sio.emit("connect", f"Connected as {sid}")


# listening to a 'message' event from the client
@sio.on("message")
async def print_message(sid, data):
    print("Socket ID", sid)
    chat_id = "bd"
    await sio.emit("new_message", data, room=chat_id)


@sio.on("disconnect")
async def disconnect(sid):
    print("SocketIO disconnect")