# human_tracker.py
import cv2
import mediapipe as mp
import time
import math
import sys
from serial.tools import list_ports
import serial

# ---------- CONFIG ----------
CAM_INDEX = 0         # change to camera index found earlier
ARDUINO_PORT = ""     # leave empty to auto-detect
BAUD = 9600

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

MIN_CHANGE = 3        # only send angle if change >= this (degrees)
SMOOTH_ALPHA = 0.25   # smoothing factor (0..1) higher = more responsive
MAX_MISSED_FRAMES = 30  # frames to wait before unlocking target (about 1 sec @30fps)
ANGLE_MIN = 20        # safe physical min angle for servo (adjust)
ANGLE_MAX = 160       # safe physical max angle for servo (adjust)
CENTER_ANGLE = 90

LOCK_ON_FIRST = True   # we will lock on first detected person by logic below
# ----------------------------

def find_arduino_port():
    ports = list(list_ports.comports())
    if not ports:
        return None
    # prefer ports with 'Arduino' in description if present
    for p in ports:
        if 'Arduino' in (p.description or ""):
            return p.device
    return ports[0].device

def map_x_to_angle(x, frame_w):
    # map x in [0, frame_w] to angle in [ANGLE_MIN, ANGLE_MAX]
    frac = max(0.0, min(1.0, x / frame_w))
    ang = int(ANGLE_MIN + frac * (ANGLE_MAX - ANGLE_MIN))
    return ang

def open_serial(port):
    try:
        s = serial.Serial(port, BAUD, timeout=1)
        time.sleep(2)  # allow Arduino reset
        print(f"[SERIAL] Opened {port}")
        return s
    except Exception as e:
        print("[ERROR] Could not open serial port:", e)
        return None

def main():
    global CAM_INDEX, ARDUINO_PORT

    # auto-detect Arduino port if not provided
    if not ARDUINO_PORT:
        ARDUINO_PORT = find_arduino_port()
        if not ARDUINO_PORT:
            print("[ERROR] No serial ports found. Connect Arduino and try again.")
            return

    arduino = open_serial(ARDUINO_PORT)
    if arduino is None:
        return

    # mediapipe pose (single-person mode, robust)
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(CAM_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    locked = False
    missed_frames = 0
    prev_angle = CENTER_ANGLE
    target_id = None  # logical placeholder (MediaPipe doesn't give IDs)
    print("[INFO] Starting. Press 'q' in window to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Camera read failed.")
                break

            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            if results.pose_landmarks:
                # we treat pose_landmarks as the "detected person"
                missed_frames = 0
                if not locked:
                    locked = True
                    print("[LOCK] New target locked")

                # compute body center: average of left & right shoulders if available
                lm = results.pose_landmarks.landmark
                left_sh = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_sh = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                # fallback to nose if shoulders not reliable
                if left_sh.visibility < 0.2 or right_sh.visibility < 0.2:
                    nose = lm[mp_pose.PoseLandmark.NOSE]
                    cx = int(nose.x * w)
                    cy = int(nose.y * h)
                else:
                    cx = int((left_sh.x + right_sh.x) / 2 * w)
                    cy = int((left_sh.y + right_sh.y) / 2 * h)

                # draw
                cv2.circle(frame, (cx, cy), 6, (0,255,0), -1)
                cv2.putText(frame, "LOCKED TARGET", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

                # map center x to servo angle
                measured_angle = map_x_to_angle(cx, w)

                # smoothing
                angle = int(SMOOTH_ALPHA * measured_angle + (1 - SMOOTH_ALPHA) * prev_angle)

                # clamp
                angle = max(ANGLE_MIN, min(ANGLE_MAX, angle))

                # send only when change is significant
                if abs(angle - prev_angle) >= MIN_CHANGE:
                    msg = f"{angle}\n".encode()
                    try:
                        arduino.write(msg)
                    except Exception as e:
                        print("[ERROR] Serial write:", e)
                        # don't exit; try again next loop
                    prev_angle = angle

                # show angle on frame
                cv2.putText(frame, f"Angle:{angle}", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)

            else:
                # no person detected
                if locked:
                    missed_frames += 1
                    cv2.putText(frame, f"LOST TARGET in {missed_frames}/{MAX_MISSED_FRAMES}", (10,30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                    if missed_frames > MAX_MISSED_FRAMES:
                        locked = False
                        print("[UNLOCK] Target lost -> looking for new person")
                else:
                    cv2.putText(frame, "No target - waiting", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

            cv2.imshow("Human Tracker (press q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\n[STOP] Keyboard interrupt")

    finally:
        cap.release()
        pose.close()
        cv2.destroyAllWindows()
        if arduino:
            arduino.close()
        print("[CLEANUP] Exited.")

if __name__ == "__main__":
    main()
