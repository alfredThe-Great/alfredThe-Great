import cv2

# Load the Haar Cascade file
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Open webcam (use 0 or /dev/video0 for Raspberry Pi)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print(" Camera not opened")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print(" Failed to grab frame")
        break

    # Convert to grayscale (faster for detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Draw rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show the result
    cv2.imshow("Face Detection", frame)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
