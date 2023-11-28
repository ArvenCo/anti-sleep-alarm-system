from imports import *
from server.controller.system import *
import server.controller.users as UserController
import server.controller.events as EventController

socketio = SocketIO(cors_allowed_origins="*")




@socketio.on('camera_stream')
def camera_stream(json):

    matt_img= base64_to_matt(json['frame'])
    data = process(matt_img)
    user = UserController.insert(json['user'])
    
    data.update({
        'img': matt_to_base64(matt_img)
    })
    
    if float(data['eye']) > 5:
        
        emit('notif-eye', data['eye'], broadcast=True) 

    if float(data['mouth']) < 1:
        emit('notif-mouth', data['mouth'], broadcast=True)
        
    if float(data['face']) > 1:
        emit('notif-face', data['face'], broadcast=True)

    # Send the processed frame back to the client
    emit('camera_stream_response', data, broadcast=True)

