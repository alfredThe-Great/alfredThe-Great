import cv2

# Open webcam (change 0 to 1 if needed)
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

print("Press 'r' to start/stop recording, 'q' to quit.")

recording = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Webcam", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):  # toggle recording
        recording = not recording
        if recording:
            print("Recording started...")
        else:
            print("Recording stopped...")

    if recording:
        out.write(frame)

    if key == ord('q'):  # quit
        break

cap.release()
out.release()
cv2.destroyAllWindows()
