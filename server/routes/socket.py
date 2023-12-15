from imports import *
from server.controller.system import *
import server.controller.users as UserController
import server.controller.events as EventController

socketio = SocketIO(cors_allowed_origins="*")


@socketio.on('stream')
def stream(data):
    video = cv.VideoCapture(data["link"])
    session["start_minute"] = time.time()
    session["eopen_time"] = time.time()
    while True:
        has_frame, frame = video.read()
        if has_frame:
            data = process(frame)
            if data:
                emit("response", data)
                print(data)
                