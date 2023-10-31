import cv2 as cv
import mediapipe as mp
import time
import utils
import math
import numpy as np

# Variables
frame_counter = 0
CEF_COUNTER = 0
TOTAL_BLINKS = 0

# Constants
CLOSED_EYES_FRAME = 3
EYES_CLOSED_THRESHOLD = 1.0
FONTS = cv.FONT_HERSHEY_COMPLEX
stay_awake_displayed = False
eyes_closed_timer = 0.0

# Face bounder indices
# FACE_OVAL=[ 10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103,67, 109]

# Lips indices for Landmarks
# LIPS=[ 61, 146, 91, 181, 84, 17, 314, 405, 321, 375,291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95,185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78 ]
# LOWER_LIPS =[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
# UPPER_LIPS=[ 185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78]

# Left eyes indices
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
# LEFT_EYEBROW =[ 336, 296, 334, 293, 300, 276, 283, 282, 295, 285]

# Right eyes indices
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
# RIGHT_EYEBROW=[ 70, 63, 105, 66, 107, 55, 65, 52, 53, 46]

map_face_mesh = mp.solutions.face_mesh

# Camera object
camera = cv.VideoCapture(0)

# Landmark detection function
def landmarksDetection(img, results, draw=False):
    img_height, img_width = img.shape[:2]
    mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]
    if draw:
        [cv.circle(img, p, 2, (0, 255, 0), -1) for p in mesh_coord]
    return mesh_coord

# Euclidean distance
def euclideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
    return distance

# Blinking ratio
def blinkRatio(img, landmarks, right_indices, left_indices):
    rhDistance = euclideanDistance(landmarks[right_indices[0]], landmarks[right_indices[8]])
    rvDistance = euclideanDistance(landmarks[right_indices[12]], landmarks[right_indices[4]])
    lhDistance = euclideanDistance(landmarks[left_indices[0]], landmarks[left_indices[8]])
    lvDistance = euclideanDistance(landmarks[left_indices[12]], landmarks[left_indices[4]])
    reRatio = rhDistance / rvDistance
    leRatio = lhDistance / lvDistance
    ratio = (reRatio + leRatio) / 2
    return ratio

with map_face_mesh.FaceMesh(min_detection_confidence=0.9, min_tracking_confidence=0.9) as face_mesh:
    start_time = time.time()
    eopen_time = 0
    eclose_time = 0
    eyes_closed_start_time = None

    while True:
        frame_counter += 1
        ret, frame = camera.read()
        if not ret:
            break

        frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_CUBIC)
        frame_height, frame_width = frame.shape[:2]
        rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            mesh_coords = landmarksDetection(frame, results, True)
            ratio = blinkRatio(frame, mesh_coords, RIGHT_EYE, LEFT_EYE)

            utils.colorBackgroundText(frame, f'Ratio: {round(ratio, 2)}', FONTS, 0.7, (30, 100), 2, utils.PINK, utils.YELLOW)

            if ratio > 5.5:
                CEF_COUNTER += 1

                if eclose_time > 0:
                    eclose_time = 0

                if eyes_closed_start_time is None:
                    eyes_closed_start_time = time.time()

                if eyes_closed_start_time is not None:
                    elapsed_time = time.time() - eyes_closed_start_time

                    if elapsed_time > EYES_CLOSED_THRESHOLD:
                        if not stay_awake_displayed:
                            print("Stay awake!")
                            stay_awake_displayed = True
                    else:
                        stay_awake_displayed = False

                    eyes_closed_timer = elapsed_time

                print(eclose_time)
            else:
                eopen_time = time.time()

                if CEF_COUNTER >= CLOSED_EYES_FRAME:
                    TOTAL_BLINKS += 1
                    CEF_COUNTER = 0

                eyes_closed_timer = 0.0
                stay_awake_displayed = False

            utils.colorBackgroundText(frame, f'Total Blinks: {TOTAL_BLINKS}', FONTS, 0.7, (30, 150), 2)
            utils.colorBackgroundText(frame, f'Eye Open(sec): {eopen_time}', FONTS, 0.7, (30, 200), 2)
            utils.colorBackgroundText(frame, f'Eye Close(sec): {eclose_time}', FONTS, 0.7, (30, 250), 2)
            cv.polylines(frame, [np.array([mesh_coords[p] for p in LEFT_EYE], dtype=np.int32)], True, utils.GREEN, 1, cv.LINE_AA)
            cv.polylines(frame, [np.array([mesh_coords[p] for p in RIGHT_EYE], dtype=np.int32)], True, utils.GREEN, 1, cv.LINE_AA)

        end_time = time.time() - start_time
        fps = frame_counter / end_time

        frame = utils.textWithBackground(frame, f'FPS: {round(fps, 1)}', FONTS, 1.0, (30, 50), bgOpacity=0.9, textThickness=2)
        cv.imshow('camera', frame)
        key = cv.waitKey(2)
        if key == ord('q') or key == ord('Q'):
            break

    cv.destroyAllWindows()
    camera.release()
