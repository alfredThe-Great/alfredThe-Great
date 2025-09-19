import cv2
import mediapipe as mp
import serial
import time

# ---------------- Arduino Setup ----------------
arduino = serial.Serial('COM3', 9600, timeout=1)  # Change COM3 to your port
time.sleep(2)  # wait for Arduino to reset

# ---------------- MediaPipe Setup ----------------
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6)

# ---------------- Camera Setup ----------------
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))

# ---------------- Servo Control Setup ----------------
servo_angle = 90
SMOOTH_ALPHA = 0.4   # Smoothing factor (lower = smoother, higher = faster response)
MIN_CHANGE = 5       # Minimum angle change before sending to Arduino

def send_angle(angle):
    """Send angle to Arduino only if changed enough"""
    global servo_angle
    if abs(angle - servo_angle) >= MIN_CHANGE:
        servo_angle = int(SMOOTH_ALPHA * angle + (1 - SMOOTH_ALPHA) * servo_angle)
        arduino.write(f"{servo_angle}\n".encode())

# ---------------- Main Loop ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # mirror effect
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        # Get nose position as reference point
        h, w, _ = frame.shape
        nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        cx = int(nose.x * w)

        # Draw circle on nose
        cv2.circle(frame, (cx, int(nose.y * h)), 8, (0, 255, 0), -1)

        # Map nose position to servo angle
        angle = int((cx / frame_width) * 180)
        send_angle(angle)

    cv2.imshow("Human Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
