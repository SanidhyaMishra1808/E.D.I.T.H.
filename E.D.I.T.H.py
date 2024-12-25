import face_recognition     # for facial landmark detection
import cv2                  # image processing
from scipy.spatial import distance as dist     # spatial distance and image processing
from threading import Thread                   # for parallel tasks
import numpy as np                             # for array operations
import pygame
import scipy.ndimage

MIN_AER = 0.30
EYE_AR_CONSEC_FRAMES = 10
COUNTER = 0
ALARM_ON = False

# sound_alarm: Initializes pygame mixer, loads the sound file, and plays it. This function is used to play an alarm sound when drowsiness is detected
def sound_alarm(soundfile):
    pygame.mixer.init()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play()

# eye_aspect_ratio: Calculates the Eye Aspect Ratio (EAR) which helps in determining if the eye is closed. It uses the distances between specific eye landmarks to compute the ratio
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# region_of_interest: Creates a mask for the region of interest in the image to focus processing on specific areas, usually for lane detection
def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

# draw_lines: Draws lines on the image. It filters lines based on slope to avoid horizontal lines and extremely steep lines, which are less likely to be lane lines
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

# process_frame: Processes the frame for lane detection. Converts the frame to grayscale, applies Gaussian blur, detects edges using Canny edge detection, 
# sharpens the edges, applies a region of interest mask, detects lines using Hough Line Transform, filters lines based on slope, and draws filtered lines on the frame
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

    # Initializes pygame mixer
    pygame.mixer.init()

    # Sets up video capture from the webcam and a video file
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 320)
    video_capture.set(4, 240)
    cap = cv2.VideoCapture('spv21.mp4')

    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    

    # Main loop to process frames from the webcam
    while True:

        # ret is a boolean indicating success, and frame is the captured image
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

            # cv2.polylines draws polylines around the eyes for visualization
            cv2.polylines(frame, [lpts], True, (255, 255, 0), 1)
            cv2.polylines(frame, [rpts], True, (255, 255, 0), 1)


            # 
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

            # if ret: processes the lane frame with process_frame and resizes it to match the drowsiness detection frame size
            if ret:
                frame_with_lines = process_frame(lane_frame)
                frame_with_lines = cv2.resize(frame_with_lines, (frame.shape[1], frame.shape[0]))
            else:
                frame_with_lines = np.zeros_like(frame)


        # combined_frame = np.hstack((frame, frame_with_lines)) stacks the drowsiness detection frame and lane detection frame side by side
        combined_frame = np.hstack((frame, frame_with_lines))

        cv2.imshow("Drowsiness and Lane Detection", combined_frame)

        # to exit frames press "q"
        if cv2.waitKey(1) == ord('q'):
            break
    
    video_capture.release()
    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()

if __name__ == '__main__':
    main()
