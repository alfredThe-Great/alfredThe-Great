import cv2

# Load the cascade you just downloaded
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Open camera
cap = cv2.VideoCapture(0)  # change to "/dev/video0" if needed
cap.set(3, 640)  # width
cap.set(4, 480)  # height

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale (Haar cascades work best in grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )

    # Draw rectangles and center points
    for (x, y, w, h) in faces:
        cx = x + w // 2
        cy = y + h // 2
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
        cv2.putText(frame, f"Face Center: {cx},{cy}", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    # Show the result
    cv2.imshow("Face Tracking", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
