from imports import *
import utils

map_face_mesh = mp.solutions.face_mesh

LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]  
OUTER_LIP = [61,185,40,39,37,0,267,269,270,409,291,375,321,405,314,17,84,181,91,146]


def landmarksDetection(img, results):
    img_height, img_width= img.shape[:2]
    # list[(x,y), (x,y)....]
    mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]
    
    # returning the list of tuples for each landmarks 
    return mesh_coord

def euclaideanDistance(point, point1, zero=False):
    x, y = point
    x1, y1 = point1
    return math.sqrt((x1 - x)**2 + (y1 - y)**2)

def eyesRatio(landmarks):
    # Right eyes 
    # horizontal line 
    rh_right = landmarks[33]
    rh_left = landmarks[133]
    # vertical line 
    rv_top = landmarks[159]
    rv_bottom = landmarks[145]

    # LEFT_EYE 
    # horizontal line 
    lh_right = landmarks[362]
    lh_left = landmarks[263]

    # vertical line 
    lv_top = landmarks[386]
    lv_bottom = landmarks[374]

    rhDistance = euclaideanDistance(rh_right, rh_left)
    rvDistance = euclaideanDistance(rv_top, rv_bottom)

    lvDistance = euclaideanDistance(lv_top, lv_bottom)
    lhDistance = euclaideanDistance(lh_right, lh_left)

    reRatio = rhDistance/rvDistance
    leRatio = lhDistance/lvDistance

    ratio = (reRatio+leRatio)/2
    return ratio

def mouthRatio(landmarks):
    # horizontal line
    mh_right = landmarks[61]
    mh_left = landmarks[291]
    # vertical line 
    mv_top = landmarks[0]
    mv_bottom = landmarks[17]
    return euclaideanDistance(mh_right, mh_left, True) / euclaideanDistance(mv_top, mv_bottom, True)

def eyesRatio_que(landmarks, que: Queue):
    que.put(eyesRatio(landmarks))

def mouthRatio_que(landmarks, que: Queue):
    que.put(mouthRatio(landmarks))