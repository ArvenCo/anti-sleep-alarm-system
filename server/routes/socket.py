from imports import *
from server.controller.system import *
socketio = SocketIO(cors_allowed_origins=['http://127.0.0.1:5500','http://192.168.1.5:5500'])




@socketio.on('camera_stream')
def camera_stream(frame):
    # Process the frame (you can perform additional processing here)
    matt_img= base64_to_matt(frame)
    data = process(matt_img)
    
    data.update({
        'img': matt_to_base64(matt_img)
    })
    # Send the processed frame back to the client
    emit('camera_stream_response', data)

