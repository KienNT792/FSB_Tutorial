import cv2
import numpy as np
import mediapipe as mp
from config import MEDIAPIPE_CONFIG, FACE_LANDMARKS, IMAGE_PROCESSING_CONFIG

class FaceDetector:
    """
    Lớp phát hiện khuôn mặt với multiple detection methods
    """
    def __init__(self):
        # Khởi tạo MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(**MEDIAPIPE_CONFIG)
        
        # Backup detector với Haar Cascade
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
        except:
            self.face_cascade = None
    
    def detect_landmarks(self, rgb_image):
        """
        Phát hiện 468 điểm mốc khuôn mặt 3D với enhanced detection
        """
        # Method 1: MediaPipe (primary)
        results = self.face_mesh.process(rgb_image)
        
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            h, w = rgb_image.shape[:2]
            landmarks = []
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                z = landmark.z
                landmarks.append((x, y, z))
            return np.array(landmarks)
        
        # Method 2: Fallback với Haar Cascade
        if self.face_cascade is not None:
            gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=3,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            if len(faces) > 0:
                face = max(faces, key=lambda x: x[2] * x[3])
                return self._generate_synthetic_landmarks(rgb_image, face)
        
        return None
    
    def _generate_synthetic_landmarks(self, image, face_rect):
        """
        Tạo landmarks tổng hợp từ face bounding box
        """
        x, y, w, h = face_rect
        landmarks = []
        
        # Face outline - mở rộng cho người hói
        face_outline_points = []
        for i in range(17):
            px = x + (i / 16.0) * w
            py = y + h * 0.8 + np.sin(i * np.pi / 16) * h * 0.2
            face_outline_points.append([px, py, 0])
        
        # Mở rộng vùng trán lên trên 25%
        forehead_extension = h * 0.25
        for i in range(len(face_outline_points)):
            if i < 8:  # Left side
                px = face_outline_points[i][0]
                py = max(0, y - forehead_extension + (i/8) * forehead_extension)
                landmarks.append([px, py, 0])
            elif i > 8:  # Right side  
                px = face_outline_points[i][0]
                py = max(0, y - forehead_extension + ((16-i)/8) * forehead_extension)
                landmarks.append([px, py, 0])
            else:  # Center
                landmarks.append([face_outline_points[i][0], max(0, y - forehead_extension), 0])
        
        # Eyes, nose, mouth landmarks
        self._add_facial_features(landmarks, x, y, w, h)
        
        return np.array(landmarks)
    
    def _add_facial_features(self, landmarks, x, y, w, h):
        """
        Thêm các điểm landmarks cho mắt, mũi, miệng
        """
        # Eyes
        eye_left_center = [x + w * 0.3, y + h * 0.4]
        eye_right_center = [x + w * 0.7, y + h * 0.4]
        
        for i in range(6):
            angle = i * np.pi / 3
            # Left eye
            px = eye_left_center[0] + np.cos(angle) * w * 0.08
            py = eye_left_center[1] + np.sin(angle) * h * 0.05
            landmarks.append([px, py, 0])
            # Right eye
            px = eye_right_center[0] + np.cos(angle) * w * 0.08
            py = eye_right_center[1] + np.sin(angle) * h * 0.05
            landmarks.append([px, py, 0])
        
        # Nose
        nose_center = [x + w * 0.5, y + h * 0.55]
        for i in range(9):
            if i < 3:
                px = nose_center[0] + (i - 1) * w * 0.02
                py = nose_center[1] - h * 0.1 + i * h * 0.05
            else:
                angle = (i - 3) * np.pi / 3
                px = nose_center[0] + np.cos(angle) * w * 0.06
                py = nose_center[1] + np.sin(angle) * h * 0.03
            landmarks.append([px, py, 0])
        
        # Mouth
        mouth_center = [x + w * 0.5, y + h * 0.75]
        for i in range(20):
            if i < 12:
                angle = i * 2 * np.pi / 12
                px = mouth_center[0] + np.cos(angle) * w * 0.12
                py = mouth_center[1] + np.sin(angle) * h * 0.06
            else:
                angle = (i-12) * 2 * np.pi / 8
                px = mouth_center[0] + np.cos(angle) * w * 0.08
                py = mouth_center[1] + np.sin(angle) * h * 0.04
            landmarks.append([px, py, 0])
