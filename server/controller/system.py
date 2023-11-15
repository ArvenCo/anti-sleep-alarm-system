from main import *
from imports import *

def base64_to_matt(img_base64: str):
    img_data = base64.b64decode(img_base64.split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    return cv.imdecode(nparr, cv.IMREAD_COLOR)

def process(frame):
    with map_face_mesh.FaceMesh(min_detection_confidence =0.5, min_tracking_confidence=0.5) as face_mesh:
        
        rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        results  = face_mesh.process(rgb_frame)


        mesh_coords = landmarksDetection(frame, results)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        results  = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:

            frame = cv.polylines(frame,  [np.array([mesh_coords[p] for p in LEFT_EYE ], dtype=np.int32)], True, utils.GREEN, 1, cv.LINE_AA)
            frame = cv.polylines(frame,  [np.array([mesh_coords[p] for p in RIGHT_EYE ], dtype=np.int32)], True, utils.GREEN, 1, cv.LINE_AA)
            data = {
                'eye': eyesRatio(mesh_coords),
                'mouth': mouthRatio(mesh_coords),
                'img_marks': matt_to_base64(frame)
            }
            return data
        
        else: return {'message' :"No face deteceted!!"}

def matt_to_base64(matt_img):
    _, img_encoded = cv.imencode('.jpg', matt_img)
    return base64.b64encode(img_encoded.tobytes()).decode('utf-8')
    
    
    