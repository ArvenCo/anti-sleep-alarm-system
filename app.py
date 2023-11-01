
import cv2 as cv
import mediapipe as mp
import time
import math

# variables 
frame_counter =0
CEF_COUNTER =0
TOTAL_BLINKS =0

eopen_time = 0
eclose_time = 0


# constants
CLOSED_EYES_FRAME =3
FONTS =cv.FONT_HERSHEY_COMPLEX
blink_above_avg = 0.1


# Left eyes indices 
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
# LEFT_EYEBROW =[ 336, 296, 334, 293, 300, 276, 283, 282, 295, 285 ]

# right eyes indices
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]  
# RIGHT_EYEBROW=[ 70, 63, 105, 66, 107, 55, 65, 52, 53, 46 ]

# inner lip indices
INNER_LIP = [78,191,80,81,82,13,312,311,310,415,308,324,318,402,317,14,87,178,88,95]

map_face_mesh = mp.solutions.face_mesh
# camera object 
camera = cv.VideoCapture(0)
# landmark detection function 
def landmarksDetection(img, results, draw=False):
    img_height, img_width= img.shape[:2]
    # list[(x,y), (x,y)....]
    mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]
    if draw :
        [cv.circle(img, p, 2, (0,255,0), -1) for p in mesh_coord]

    # returning the list of tuples for each landmarks 
    return mesh_coord

# Euclaidean distance 
def euclaideanDistance(point, point1, zero = False):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
    if distance == 0 and zero:
        distance = 0.00000001
    return distance

# Blinking Ratio
def blinkRatio(img, landmarks, right_indices, left_indices):
    # Right eyes 
    # horizontal line 
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]
    # vertical line 
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]

    # LEFT_EYE 
    # horizontal line 
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]

    # vertical line 
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]

    rhDistance = euclaideanDistance(rh_right, rh_left)
    rvDistance = euclaideanDistance(rv_top, rv_bottom)

    lvDistance = euclaideanDistance(lv_top, lv_bottom)
    lhDistance = euclaideanDistance(lh_right, lh_left)

    reRatio = rhDistance/rvDistance
    leRatio = lhDistance/lvDistance

    ratio = (reRatio+leRatio)/2
    return ratio 


def yawnRatio(img, landmarks, indeces):
    # horizontal line
    inner_right = landmarks[indeces[0]]
    inner_left = landmarks[indeces[10]]

    # vertical line
    inner_top = landmarks[indeces[5]]
    inner_bottom = landmarks[indeces[-5]]
    
    
    return  euclaideanDistance(inner_right, inner_left, zero=True)/ euclaideanDistance(inner_top, inner_bottom, zero=True)

with map_face_mesh.FaceMesh(min_detection_confidence =0.9, min_tracking_confidence=0.9) as face_mesh:

    # starting Video loop here.
    while True:
        frame_counter += 1

        ret, frame = camera.read() # getting frame from camera 
        if not ret: 
            break # no more frames break

        #  resizing frame
        frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_CUBIC)
        frame_height, frame_width= frame.shape[:2]
        rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        results  = face_mesh.process(rgb_frame)
        
        
        
        if results.multi_face_landmarks:
            mesh_coords = landmarksDetection(frame, results)
            blink = blinkRatio(frame, mesh_coords, RIGHT_EYE, LEFT_EYE) 


            if blink > 5.5:
                CEF_COUNTER +=1
                eclose_time = time.time() - eopen_time
                # print(eclose_time)
                if eclose_time > blink_above_avg:
                    print("Stay Awake")
            else:
                eopen_time = time.time()
                eclose_time = 0
                
                if CEF_COUNTER>CLOSED_EYES_FRAME:
                    TOTAL_BLINKS += 1
                    CEF_COUNTER = 0
                    
            
            # if yawnRatio(frame, mesh_coords, INNER_LIP) < 2:
            #     print('YAWNING!!!!!!!!!!!!!!!!!!')
            
            
                
               
        
        
        print(f'fps: {frame_counter/time.time()}')
        
    cv.destroyAllWindows()
    camera.release()