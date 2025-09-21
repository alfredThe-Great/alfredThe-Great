import cv2
import mediapipe as mp
import serial
import time

# ---------------- Arduino Setup ----------------
arduino = serial.Serial('COM3', 9600, timeout=1)  # Change COM3 if needed
time.sleep(2)

# ---------------- MediaPipe Setup ----------------
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6)

# ---------------- Camera Setup ----------------
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))

# ---------------- Servo Control Setup ----------------
servo_angle = 90
SMOOTH_ALPHA = 0.4
MIN_CHANGE = 5

def send_angle(angle):
    global servo_angle
    if abs(angle - servo_angle) >= MIN_CHANGE:
        servo_angle = int(SMOOTH_ALPHA * angle + (1 - SMOOTH_ALPHA) * servo_angle)
        arduino.write(f"{servo_angle}\n".encode())

# ---------------- Main Loop ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ✅ Remove mirror effect (don’t flip)
    # frame = cv2.flip(frame, 1)  # <--- REMOVED

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        h, w, _ = frame.shape
        nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        cx = int(nose.x * w)

        cv2.circle(frame, (cx, int(nose.y * h)), 8, (0, 255, 0), -1)

        # ✅ Invert mapping so servo moves correctly
        angle = int((1 - (cx / frame_width)) * 180)
        send_angle(angle)

    cv2.imshow("Human Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
