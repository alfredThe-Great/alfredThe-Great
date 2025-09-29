import cv2
import mediapipe as mp
import serial
import time

# Connect to Arduino (change COM3 to your port)
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # give time to reset

# Mediapipe face detection setup
mp_face = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils
face_detection = mp_face.FaceDetection(0.7)

# Webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(frame_rgb)

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            cx = int(bboxC.xmin * w + bboxC.width * w / 2)

            # Draw box for visualization
            mp_draw.draw_detection(frame, detection)

            # Face position relative to center
            if cx < w // 3:  
                arduino.write(b"L")  # Move Left
            elif cx > 2 * w // 3:
                arduino.write(b"R")  # Move Right
            else:
                arduino.write(b"S")  # Stop
    else:
        arduino.write(b"S")  # No face → Stop

    cv2.imshow("Face Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
