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
            data = ""
            int_session("TOTAL_BLINKS")

            # blinking 
            if eyesRatio(mesh_coords) >5:
                int_session("CEF_COUNTER", 1)
                print("blink")
                session["eclose_time"] = time.time() - session["eopen_time"]
                
                last_close_sec = session["eclose_time"]
                # cv.putText(frame, 'Blink', (200, 50), FONTS, 1.3, utils.PINK, 2)
                
                
                if session["eclose_time"] > 0.5:
                    data = "Sleeping"
                    # utils.colorBackgroundText(frame,  f'SLEEPING!!', FONTS, 1.7, (int(frame_height/2), 200), 2, utils.YELLOW, pad_x=6, pad_y=6, )
            else:
                session["eopen_time"] = time.time()
                session["eclose_time"] = 0
                
                if session.get("CEF_COUNTER", 0)>2:
                    # utils.colorBackgroundText(frame,  f'Blink', FONTS, 1.7, (int(frame_height/2), 100), 2, utils.YELLOW, pad_x=6, pad_y=6, )
                    data = "Blinked"
                    session["TOTAL_BLINKS"] += 1
                    session["CEF_COUNTER"] = 0


            # Blink per minute
            session["elapsed_time"] = time.time() - session["start_minute"]
            if session["elapsed_time"] >= 60:
                blink_pm = (session["TOTAL_BLINKS"] / session["elapsed_time"]) * 60
                
                session["TOTAL_BLINKS"] = 0
                session["CEF_COUNTER"] = 0
                session["start_minute"] = time.time()
                if blink_pm <= 5:
                    data = "Drowsy"
                else:
                    data = "Active"

                
            
            if mouthRatio(mesh_coords) < 1 :
                session["mouth_time"] = time.time()
                data = "Yawning"
            
            
            
            return data
        
        else: 
            return "No face deteceted"

def distance(start, current):
    return current - start

def check_session(key):
    return key in session

def int_session(key, time_float = 0):
    if check_session(key) != True:
        session[key] = 0
    else:
        session[key] += time_float
    return session[key]
    

def matt_to_base64(matt_img):
    _, img_encoded = cv.imencode('.jpg', matt_img)
    return base64.b64encode(img_encoded.tobytes()).decode('utf-8')
    
    
    