import cv2
import mediapipe as mp
import serial, time

# === Arduino setup ===
arduino = serial.Serial('COM3', 9600)  # change COM3 to your Arduino port
time.sleep(2)

# === MediaPipe setup ===
mp_face = mp.solutions.face_detection
face_detector = mp_face.FaceDetection(min_detection_confidence=0.6)

cap = cv2.VideoCapture(0)  # 0 = laptop camera, 1 = USB webcam
prev_angle = 90  # start centered
SMOOTH_ALPHA = 0.2   # smoothing factor
MIN_CHANGE = 3       # ignore small changes

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detector.process(rgb)

    h, w, _ = frame.shape
    if results.detections:
        # pick the largest face
        best = max(results.detections, key=lambda d: d.location_data.relative_bounding_box.width)
        bbox = best.location_data.relative_bounding_box

        cx = int((bbox.xmin + bbox.width / 2) * w)

        # map cx to 0–180
        target_angle = int((cx / w) * 180)

        # smooth + filter noise
        angle = int(SMOOTH_ALPHA * target_angle + (1 - SMOOTH_ALPHA) * prev_angle)
        if abs(angle - prev_angle) >= MIN_CHANGE:
            arduino.write(f"{angle}\n".encode())
            prev_angle = angle

        # draw visuals
        cv2.circle(frame, (cx, h // 2), 5, (0, 0, 255), -1)
        cv2.putText(frame, f"Servo: {angle}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.imshow("Face Tracker (1 Servo)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
