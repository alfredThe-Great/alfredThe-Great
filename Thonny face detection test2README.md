import cv2

# Load face detector from the downloaded XML file
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
if face_cascade.empty():
    print("Failed to load cascade. Please check the file name and path.")
    exit()

# Open your working webcam device
cap = cv2.VideoCapture("/dev/video10")
if not cap.isOpened():
    print("Cannot open webcam (/dev/video10)")
    exit()

# Optional: reduce resolution for better performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Starting face detection. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50,50))
    print(f"Detected {len(faces)} face(s)")

    for (x, y, w, h) in faces:
        cx, cy = x + w//2, y + h//2
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.circle(frame, (cx, cy), 5, (255,0,0), -1)
        cv2.putText(frame, f"Center: {cx},{cy}", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imshow("Face Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
