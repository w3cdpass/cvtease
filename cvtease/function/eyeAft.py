import json
import cv2
import mediapipe as mp
import numpy as np
import math

# Load the PNG file paths from JSON
with open('cvtease/database/eyeAftjson.json', 'r') as file:
    data = json.load(file)
glasses_paths = data['images']

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
current_glasses_img = cv2.imread(glasses_paths[0], cv2.IMREAD_UNCHANGED)

def load_glasses_image(path):
    global current_glasses_img
    current_glasses_img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

def overlay_image_alpha(img, img_overlay, pos, alpha_mask):
    x, y = pos

    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis] / 255.0
    img[y1:y2, x1:x2] = (1.0 - alpha) * img[y1:y2, x1:x2] + alpha * img_overlay[y1o:y2o, x1o:x2o]

def apply_glasses(image, landmarks):
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    glasses_width = int(math.dist([left_eye.x, left_eye.y], [right_eye.x, right_eye.y]) * image.shape[1] * 1.5)
    glasses_height = int(glasses_width * current_glasses_img.shape[0] / current_glasses_img.shape[1])

    resized_glasses = cv2.resize(current_glasses_img, (glasses_width, glasses_height), interpolation=cv2.INTER_AREA)

    center_x = int((left_eye.x + right_eye.x) / 2 * image.shape[1])
    center_y = int((left_eye.y + right_eye.y) / 2 * image.shape[0])

    x = center_x - glasses_width // 2
    y = center_y - glasses_height // 2 - int(0.1 * glasses_height)

    overlay_image_alpha(image, resized_glasses[:, :, 0:3], (x, y), resized_glasses[:, :, 3])
