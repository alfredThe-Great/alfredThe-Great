import cv2

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Open webcam
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Lower resolution for faster performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

if not cap.isOpened():
    print(" Camera not opened")
    exit()

frame_count = 0
faces = []  # keep faces from last detection

while True:
    ret, frame = cap.read()
    if not ret:
        print(" Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect only every 3rd frame
    if frame_count % 3 == 0:
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Draw rectangle around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Face Detection (Optimized)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

cap.release()
cv2.destroyAllWindows()
