import cv2
import mediapipe as mp
import math

def open_camera(facial_keypoints=False):
    # Initialize mediapipe face mesh
    mp_face_detection = mp.solutions.face_detection
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

    # Open the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image and find faces
        face_detection_results = face_detection.process(rgb_frame)

        # Draw rectangle around the faces and detect facial keypoints if enabled
        if face_detection_results.detections:
            for detection in face_detection_results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle for detected face

                if facial_keypoints:
                    face_mesh_results = face_mesh.process(rgb_frame)
                    if face_mesh_results.multi_face_landmarks:
                        for face_landmarks in face_mesh_results.multi_face_landmarks:
                            mp_drawing.draw_landmarks(
                                image=frame,
                                landmark_list=face_landmarks,
                                connections=mp_face_mesh.FACEMESH_TESSELATION,
                                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1),
                                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                            )

                            # Estimate distance from camera based on face width
                            face_width_in_frame = w
                            # Constants for focal length and known face width (in centimeters)
                            focal_length = 500  # This is an example value, adjust it for your setup
                            known_face_width = 15  # Average human face width in cm
                            distance = (known_face_width * focal_length) / face_width_in_frame
                            cv2.putText(frame, f'Distance: {distance:.2f} cm', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Display the resulting frame
        cv2.imshow('Face Detection', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()
