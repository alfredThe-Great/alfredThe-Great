import cv2

# Open webcam (/dev/video0 is default)
cap = cv2.VideoCapture(0)

# Lower resolution for Raspberry Pi (faster, smaller files)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 15.0, (320, 240))  # lower FPS & resolution

print("Press 'r' to start/stop recording, 'q' to quit.")

recording = False

while True:
    ret, frame = cap.read()
    if not ret:
        print(" Failed to grab frame")
        break

    cv2.imshow("Webcam", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):  # toggle recording
        recording = not recording
        if recording:
            print(" Recording started...")
        else:
            print(" Recording stopped...")

    if recording:
        out.write(frame)

    if key == ord('q'):  # quit
        break

cap.release()
out.release()
cv2.destroyAllWindows()
