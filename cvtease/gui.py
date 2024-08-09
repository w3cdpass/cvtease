import sys
import os
import cv2
import mediapipe as mp
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QSlider, QComboBox
)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, Qt, QDir, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class FaceDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Detection App")
        self.setGeometry(100, 100, 800, 600)

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1, refine_landmarks=True,
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Start Camera", self)
        self.start_button.clicked.connect(self.start_camera)

        self.stop_button = QPushButton("Stop Camera", self)
        self.stop_button.clicked.connect(self.stop_camera)

        self.capture_button = QPushButton("Capture Photo", self)
        self.capture_button.clicked.connect(self.capture_photo)

        # Load the capture sound using QMediaPlayer
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setSource(QUrl.fromLocalFile("cvtease/asset/photoCapture.wav"))  # Update the path to your sound file

        # Settings Panel
        self.settings_panel = QWidget() 
        self.settings_layout = QVBoxLayout()

        self.slider_detection = QSlider(Qt.Horizontal)
        self.slider_detection.setRange(0, 100)
        self.slider_detection.setValue(50)
        self.slider_detection.setTickInterval(10)
        self.slider_detection.setTickPosition(QSlider.TicksBelow)
        self.slider_detection.valueChanged.connect(self.update_detection_confidence)

        self.label_detection = QLabel("Detection Confidence: 0.5")
        self.settings_layout.addWidget(self.label_detection)
        self.settings_layout.addWidget(self.slider_detection)

        self.combo_box_connections = QComboBox()
        self.combo_box_connections.addItem("Tesselation")
        self.combo_box_connections.addItem("Contours")
        self.combo_box_connections.addItem("Iris")
        self.combo_box_connections.currentIndexChanged.connect(self.update_connections)

        self.settings_layout.addWidget(self.combo_box_connections)
        self.settings_panel.setLayout(self.settings_layout)

        # Under Development Label
        self.dev_label = QLabel("This tool is under development. Please be patient.", self)
        self.dev_label.setAlignment(Qt.AlignCenter)
        self.dev_label.setStyleSheet("color: red; font-weight: bold;")

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.capture_button)  # Add the capture photo button
        layout.addWidget(self.settings_panel)
        layout.addWidget(self.dev_label)  # Add the development label

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_camera(self):
        self.capture.open(0)
        self.timer.start(30)

    def stop_camera(self):
        self.timer.stop()
        self.capture.release()
        self.image_label.clear()

    def update_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.draw_face_landmarks(frame, face_landmarks)

        q_img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def draw_face_landmarks(self, image, face_landmarks):
        connections = self.get_connections_from_combo()
        self.mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=connections,
            landmark_drawing_spec=None,
            connection_drawing_spec=self.mp_drawing_styles
            .get_default_face_mesh_tesselation_style())

    def update_detection_confidence(self, value):
        confidence = value / 100.0
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1, refine_landmarks=True,
            min_detection_confidence=confidence, min_tracking_confidence=0.5)
        self.label_detection.setText(f"Detection Confidence: {confidence}")

    def update_connections(self):
        self.update_frame()

    def get_connections_from_combo(self):
        index = self.combo_box_connections.currentIndex()
        if index == 0:
            return mp.solutions.face_mesh.FACEMESH_TESSELATION
        elif index == 1:
            return mp.solutions.face_mesh.FACEMESH_CONTOURS
        elif index == 2:
            return mp.solutions.face_mesh.FACEMESH_IRISES

    def capture_photo(self):
        # Capture a fresh frame to avoid blurriness
        ret, frame = self.capture.read()
        if not ret:
            print("Failed to capture frame")
            return

        # Convert the frame to RGB to match display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Play the capture sound
        self.media_player.play()

        # Save to the user's Downloads directory
        downloads_path = os.path.join(QDir.homePath(), "Downloads")
        if not os.path.exists(downloads_path):
            os.makedirs(downloads_path)
        photo_path = os.path.join(downloads_path, "captured_photo.jpg")

        cv2.imwrite(photo_path, frame_rgb)
        print(f"Photo captured and saved as {photo_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceDetectionApp()
    window.show()
    sys.exit(app.exec())