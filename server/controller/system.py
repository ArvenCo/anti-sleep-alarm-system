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



        rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        results  = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            mesh_coords = landmarksDetection(frame, results)
            data = dict()
            
            if eyesRatio(mesh_coords) > 5 and "eye_time" not in session or distance(session["eye_time"], time.time()) < .5:
                int_session("eye_time")
                
                
                int_session(session["eye_elap_time"], distance(session["eye_time"], time.time())) 
                if session["eye_elap_time"] >= 60:
                    bpm = (session["blink"] / session["eye_elap_time"]) * 60
                    if bpm <= 5:
                        data["eye_status"] = "DROWSY"
                        
                elif session["eye_elap_time"] >=1 :
                    int_session("blink", 1)

                
                
                session["eye_time"] = time.time()
                
            
            if mouthRatio(mesh_coords) < 1 and "mouth_time" not in session or distance(session["mouth_time"], time.time()) < .5:
                session["mouth_time"] = time.time()
            
            
            
            # data = {
            #     'eye': eyesRatio(mesh_coords),
            #     'mouth': mouthRatio(mesh_coords),
            #     'face': faceRatio(mesh_coords),
            # }
            return data
        
        else: return {'message' :"No face deteceted!!"}

def distance(prev, now):
    return now - prev

def check_session(key):
    return key in session

def int_session(key, time_float = 0):
    if check_session(key) != True:
        session[key] = 0
    else:
        session[key] += time_float
    

def matt_to_base64(matt_img):
    _, img_encoded = cv.imencode('.jpg', matt_img)
    return base64.b64encode(img_encoded.tobytes()).decode('utf-8')
    
    
    