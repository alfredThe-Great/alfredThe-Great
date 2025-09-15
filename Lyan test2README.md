import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Open camera (0 = default). You can change to 1,2 if you have multiple cameras.
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # PC can handle 640x480 comfortably
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    print("Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # MediaPipe expects RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)

        if results.detections:
            for i, det in enumerate(results.detections):
                # Draw box and keypoints using MediaPipe helper
                mp_drawing.draw_detection(frame, det)

                # bounding box (relative coords)
                bbox = det.location_data.relative_bounding_box
                h, w, _ = frame.shape
                x1 = int(bbox.xmin * w)
                y1 = int(bbox.ymin * h)
                box_w = int(bbox.width * w)
                box_h = int(bbox.height * h)

                # compute center
                cx = x1 + box_w // 2

                # determine left/center/right relative to frame
                if cx < w * 0.33:
                    pos = "Looking Left"
                elif cx > w * 0.66:
                    pos = "Looking Right"
                else:
                    pos = "Center"

                # confidence
                conf = int(det.score[0] * 100)

                # label
                label = f"Face {i+1}: {conf}% - {pos}"
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # show frame
        cv2.imshow("MediaPipe Face Descriptions", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
