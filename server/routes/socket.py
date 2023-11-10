from imports import *

socketio = SocketIO()

@socketio.on('connect')
def connect():
    return