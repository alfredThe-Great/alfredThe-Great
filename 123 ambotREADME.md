import cv2
import imutils
from gpiozero import Servo
from time import sleep

# Initialize servo on GPIO18
servo = Servo(18)

# Servo range: -1 (full left) to 1 (full right)
servo_pos = 0
servo.value = servo_pos

# Initialize webcam
cap = cv2.VideoCapture(0)

# Use HOG-based people detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect people
    boxes, weights = hog.detectMultiScale(gray, winStride=(8,8))

    if len(boxes) > 0:
        # Take first person detected
        (x, y, w, h) = boxes[0]
        person_center_x = x + w // 2
        frame_center_x = frame.shape[1] // 2

        # Difference from center
        error = person_center_x - frame_center_x

        if abs(error) > 20:  # Dead zone
            if error > 0:
                servo_pos -= 0.05  # turn right
            else:
                servo_pos += 0.05  # turn left

            # Clamp values
            servo_pos = max(-1, min(1, servo_pos))
            servo.value = servo_pos

        # Draw detection box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

    cv2.imshow("Human Following Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
