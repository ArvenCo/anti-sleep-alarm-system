from imports import *
from server.controller.system import *
import server.controller.users as UserController
import server.controller.events as EventController

socketio = SocketIO(cors_allowed_origins="*")


@socketio.on('stream')
def stream(data):
    video = cv.VideoCapture(data["link"])
    while True:
        has_frame, frame = video.read()
        if has_frame:
            data = process(frame)
            emit("response", data)
            



@socketio.on('camera_stream')
def camera_stream(data):
    matt_img= base64_to_matt(data['frame'])
    data = process(matt_img)
    # user = UserController.insert()
    
    data.update({
        'img': matt_to_base64(matt_img)
    })
    open_eye = 0
    
    emit('response', "image received")
    # if float(data['eye']) > 5:
    #     emit('response', data['eye'], broadcast=True) 
    #     close_eye = time.time() - open_eye
    #     if close_eye > 0.5:
    #         # eyes closed 
    #         pass
    #     else:
    #         # blinking
    #         pass
    # else:
    #     open_eye = time.time() 

    # if float(data['mouth']) < 1:
    #     emit('response', data['mouth'], broadcast=True)
        
    # if float(data['face']) > 1:
    #     emit('response', data['face'], broadcast=True)

    
    # Send the processed frame back to the client
    emit('camera_stream_response', data, broadcast=True)

