import cv2 as cv
import mediapipe as mp
import time

# Open webcam
capture = cv.VideoCapture(0, cv.CAP_DSHOW)

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=False
)

mp_drawing = mp.solutions.drawing_utils
prev_time = 0

while True:
    isTrue, frame = capture.read()
    if not isTrue:
        break

    # Flip for mirror view (optional)
    frame = cv.flip(frame, 1)

    # Convert BGR to RGB (MediaPipe needs RGB)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    frame_height, frame_width, _ = frame.shape

    curr_time = time.time()
    fps = int(1 / (curr_time - prev_time))
    prev_time = curr_time
    cv.putText(frame, f'FPS: {fps}', (20, 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255 , 255), 2)

    # Define boundaries
    left_boundary = int(frame_width * 0.40)
    right_boundary = int(frame_width * 0.60)

    # Draw vertical guide lines
    cv.line(frame, (left_boundary, 0), (left_boundary, frame_height), (0,0,225), 2)
    cv.line(frame, (right_boundary,0), (right_boundary, frame_height), (0,0,255), 2)

    status = "No Face"
    color = (0, 255, 255)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            # Get nose landmark (index 1)
            nose = face_landmarks.landmark[1]

            nose_x = int(nose.x * frame_width)
            nose_y = int(nose.y * frame_height)

            # Draw nose point
            cv.circle(frame, (nose_x, nose_y), 3, (255, 255, 0), 1)

            # Threshold logic
            if nose_x < left_boundary or nose_x > right_boundary:
                status = "Not Attentive"
                color = (0, 0, 255)
            else:
                status = "Attentive"
                color = (0, 255, 0)

    cv.putText(frame, status, (20, 60),
               cv.FONT_HERSHEY_SIMPLEX,
               1,
               color,
               2)

    cv.imshow("MediaPipe Face Alignment", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()