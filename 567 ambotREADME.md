import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open camera")
    exit()

ret, frame = cap.read()
if ret:
    cv2.imwrite("photo.jpg", frame)
    print("✅ Photo saved as photo.jpg")
else:
    print("❌ Failed to grab frame")

cap.release()
