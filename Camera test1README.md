import cv2

# Try different devices: /dev/video0, /dev/video1, /dev/video10, etc.
devices = ["/dev/video0", "/dev/video1", "/dev/video10"]

for dev in devices:
    print(f"🔍 Testing {dev} ...")
    cap = cv2.VideoCapture(dev)

    if not cap.isOpened():
        print(f"❌ Cannot open {dev}")
        continue

    ret, frame = cap.read()
    if not ret:
        print(f"⚠️ Failed to grab frame from {dev}")
        cap.release()
        continue

    print(f"✅ Success! Showing video from {dev}")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Frame grab failed")
            break

        cv2.imshow(f"Camera Test - {dev}", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    break  # stop after finding a working camera
