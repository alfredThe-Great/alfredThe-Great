import cv2

# Open webcam at low resolution
cap = cv2.VideoCapture(0)
cap.set(3, 320)  # width
cap.set(4, 240)  # height

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

print(" Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        print(" Failed to grab frame")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw rectangles
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show result
    cv2.imshow("Face Detection (Pi 3B Optimized)", frame)

    # Quit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
