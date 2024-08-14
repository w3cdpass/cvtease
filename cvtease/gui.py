import json
import sys
import os
import cv2
import mediapipe as mp
from PySide6.QtWidgets import (
    QHBoxLayout, QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QSlider, QComboBox
)
from PySide6.QtGui import QImage, QPixmap, QIcon
from PySide6.QtCore import QTimer, QDir, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from cvtease.style import style
from .function.eyeAft import apply_glasses, load_glasses_image


def apply_app_icon(app, icon_path):
    icon = QIcon(icon_path)
    app.setWindowIcon(icon)

class FaceDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(style.WINDOW_TITLE)
        self.setGeometry(*style.WINDOW_GEOMETRY)
        self.setWindowIcon(QIcon("cvtease/asset/laugh.ico"))

        self.switch_button = QPushButton("Switch Glasses", self)
        self.switch_button.setStyleSheet(style.ROUND_BUTTON_STYLE)
        self.switch_button.clicked.connect(self.switch_glasses)
        
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
        self.image_label.setAlignment(style.IMAGE_LABEL_ALIGNMENT)

        # Create and style buttons
        self.start_button = QPushButton("Start Camera", self)
        self.start_button.setStyleSheet(style.ROUND_BUTTON_STYLE)
        self.start_button.clicked.connect(self.start_camera)

        self.capture_button = QPushButton("Capture Photo", self)
        self.capture_button.setStyleSheet(style.ROUND_BUTTON_STYLE)
        self.capture_button.clicked.connect(self.capture_photo)

        self.stop_button = QPushButton("Stop Camera", self)
        self.stop_button.setStyleSheet(style.ROUND_BUTTON_STYLE)
        self.stop_button.clicked.connect(self.stop_camera)

        # Create a horizontal layout for the buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.capture_button)
        self.button_layout.addWidget(self.stop_button)

        # Load the capture sound using QMediaPlayer
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setSource(QUrl.fromLocalFile("cvtease/asset/photoCapture.wav"))

        # Settings Panel
        self.settings_panel = QWidget()
        self.settings_layout = QVBoxLayout()

        self.slider_detection = QSlider(style.SLIDER_TICK_POSITION)
        self.slider_detection.setRange(*style.SLIDER_RANGE)
        self.slider_detection.setValue(style.SLIDER_DEFAULT_VALUE)
        self.slider_detection.setTickInterval(style.SLIDER_TICK_INTERVAL)
        self.slider_detection.setTickPosition(QSlider.TicksBelow)
        self.slider_detection.setStyleSheet(style.SLIDER_STYLE)
        self.slider_detection.valueChanged.connect(self.update_detection_confidence)

        # Initialize the glasses index and paths
        with open('cvtease/database/eyeAftjson.json', 'r') as file:
            data = json.load(file)
        self.glasses_paths = data['images']
        self.glasses_index = 0
        self.current_glasses_path = self.glasses_paths[self.glasses_index]

        self.combo_box_connections = QComboBox()
        self.combo_box_connections.addItems(style.COMBO_BOX_ITEMS)
        self.combo_box_connections.setStyleSheet(style.COMBO_BOX_STYLE)
        self.combo_box_connections.currentIndexChanged.connect(self.update_connections)

        self.settings_layout.addWidget(self.combo_box_connections)
        self.settings_panel.setLayout(self.settings_layout)

        self.label_detection = QLabel(f"Detection Confidence: 0.5")
        self.settings_layout.addWidget(self.label_detection)
        self.settings_layout.addWidget(self.slider_detection)

        # Under Development Label
        self.dev_label = QLabel(style.DEV_LABEL_STYLE, self)
        self.dev_label.setAlignment(style.IMAGE_LABEL_ALIGNMENT)
        self.dev_label.setStyleSheet(style.DEV_LABEL_STYLE)

        # Create and set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(self.button_layout)  # Use the horizontal layout
        layout.addWidget(self.settings_panel)
        layout.addWidget(self.dev_label)
        layout.addWidget(self.switch_button)  # Add the switch button

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
        if connections == mp.solutions.face_mesh.FACEMESH_IRISES:
            apply_glasses(image, face_landmarks.landmark, self.current_glasses_path)
        else:
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
        ret, frame = self.capture.read()
        if not ret:
            print("Failed to capture frame")
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.media_player.play()

        downloads_path = os.path.join(QDir.homePath(), "Downloads")
        if not os.path.exists(downloads_path):
            os.makedirs(downloads_path)
        photo_path = os.path.join(downloads_path, "captured_photo.jpg")

        cv2.imwrite(photo_path, frame_rgb)
        print(f"Photo captured and saved as {photo_path}")

    def switch_glasses(self):
        # Increment the index and loop back to 0 if it exceeds the length
        self.glasses_index = (self.glasses_index + 1) % len(self.glasses_paths)
        
        # Load the new glasses image using the correct function
        load_glasses_image(self.glasses_index)
        
        # Force the frame to update with the new glasses
        self.update_frame()

        print(f"Switched to {self.glasses_paths[self.glasses_index]}")  # Force the frame to update

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply the icon to the application
    apply_app_icon(app, "cvtease/asset/laugh.ico")
    
    window = FaceDetectionApp()
    window.show()
    
    sys.exit(app.exec())
