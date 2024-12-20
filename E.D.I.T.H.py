import face_recognition
import cv2
from scipy.spatial import distance as dist
from threading import Thread
import numpy as np
import pygame
import scipy.ndimage

MIN_AER = 0.30
EYE_AR_CONSEC_FRAMES = 10
COUNTER = 0
ALARM_ON = False

def sound_alarm(soundfile):
    pygame.mixer.init()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play()

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines):
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                slope = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else np.inf
                if abs(slope) < 0.5 or abs(slope) > 2:  
                    continue
                cv2.line(blank_image, (x1, y1), (x2, y2), (0, 255, 0), thickness=5)
    
    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    sharpened = scipy.ndimage.convolve(edges, [[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    
    height, width = edges.shape
    roi_vertices = [
        (0, height),
        (width // 2 - width // 10, height // 2 + height // 10),
        (width // 2 + width // 10, height // 2 + height // 10),
        (width, height)
    ]
    
    cropped_edges = region_of_interest(sharpened, np.array([roi_vertices], np.int32))
    
    lines = cv2.HoughLinesP(
        cropped_edges,
        rho=2,
        theta=np.pi / 180,
        threshold=100,
        lines=np.array([]),
        minLineLength=80,
        maxLineGap=50
    )
    
    if lines is not None:
        filtered_lines = [line for line in lines if len(line[0]) == 4 and 0.5 < abs((line[0][3] - line[0][1]) / (line[0][2] - line[0][0])) < 2]  # Filter lines by slope
        frame_with_lines = draw_lines(frame, filtered_lines)
    else:
        frame_with_lines = frame
    
    return frame_with_lines

def main():
    global COUNTER, ALARM_ON

    pygame.mixer.init()

    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 320)
    video_capture.set(4, 240)
    
    cap = cv2.VideoCapture('spv.mp4')
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        face_landmarks_list = face_recognition.face_landmarks(frame)
        for face_landmark in face_landmarks_list:
            leftEye = face_landmark['left_eye']
            rightEye = face_landmark['right_eye']

            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            lpts = np.array(leftEye)
            rpts = np.array(rightEye)

            cv2.polylines(frame, [lpts], True, (255, 255, 0), 1)
            cv2.polylines(frame, [rpts], True, (255, 255, 0), 1)

            if ear < MIN_AER:
                COUNTER += 1
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    if not ALARM_ON:
                        ALARM_ON = True
                        t = Thread(target=sound_alarm, args=('alarm.wav',))
                        t.daemon = True
                        t.start()
                cv2.putText(frame, "Alert!", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                COUNTER = 0
                if ALARM_ON:
                    ALARM_ON = False
                    pygame.mixer.music.stop()
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if cap.isOpened():
            ret, lane_frame = cap.read()
            if ret:
                frame_with_lines = process_frame(lane_frame)
                frame_with_lines = cv2.resize(frame_with_lines, (frame.shape[1], frame.shape[0]))
            else:
                frame_with_lines = np.zeros_like(frame)

        combined_frame = np.hstack((frame, frame_with_lines))

        cv2.imshow("Drowsiness and Lane Detection", combined_frame)
        if cv2.waitKey(1) == ord('q'):
            break
    
    video_capture.release()
    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()

if __name__ == '__main__':
    main()