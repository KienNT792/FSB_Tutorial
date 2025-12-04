# Threading module for image processing

from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
from face_detector import FaceDetector
from mask_creator import MaskCreator
from image_processor import ImageProcessor, SkinEnhancer

class ProcessingThread(QThread):
    """
    Thread xử lý ảnh bất đồng bộ
    """
    # Signals
    progress = pyqtSignal(int)
    finished = pyqtSignal(np.ndarray, np.ndarray)  # processed_image, landmarks
    error = pyqtSignal(str)
    
    def __init__(self, image, strength, method, options):
        super().__init__()
        self.image = image.copy()
        self.strength = strength
        self.method = method
        self.options = options
        
        # Initialize processors
        self.face_detector = FaceDetector()
        self.mask_creator = MaskCreator()
        self.image_processor = ImageProcessor()
        self.skin_enhancer = SkinEnhancer()
    
    def run(self):
        """
        Chạy xử lý ảnh trong thread riêng
        """
        try:
            self.progress.emit(10)
            
            # 1. Tiền xử lý ảnh
            rgb_image, original_shape = self.image_processor.preprocess_image(self.image)
            processed_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
            self.progress.emit(20)
            
            # 2. Phát hiện landmarks
            landmarks = self.face_detector.detect_landmarks(rgb_image)
            self.progress.emit(40)
            
            # 3. Tạo mask vùng da
            if landmarks is not None:
                mask = self.mask_creator.create_skin_mask(processed_image, landmarks)
            else:
                # Fallback mask cho toàn bộ ảnh
                h, w = processed_image.shape[:2]
                mask = np.ones((h, w), dtype=np.float32) * 0.3
            self.progress.emit(50)
            
            # 4. Áp dụng filter chính
            if self.method == 'bilateral':
                processed_image = self.image_processor.apply_bilateral_filter(
                    processed_image, mask, self.strength
                )
            elif self.method == 'guided':
                processed_image = self.image_processor.apply_guided_filter(
                    processed_image, mask, self.strength
                )
            elif self.method == 'edge_preserve':
                processed_image = self.image_processor.apply_edge_preserving_filter(
                    processed_image, mask, self.strength
                )
            elif self.method == 'advanced':
                processed_image = self.image_processor.apply_advanced_blend(
                    processed_image, mask, self.strength
                )
            
            self.progress.emit(70)
            
            # 5. Áp dụng các enhancement nâng cao
            if self.options.get('blemish', False):
                processed_image = self.skin_enhancer.blemish_removal(
                    processed_image, landmarks, strength=0.8
                )
            
            if self.options.get('wrinkle', False):
                processed_image = self.skin_enhancer.wrinkle_reduction(
                    processed_image, landmarks, strength=0.6
                )
            
            if self.options.get('skin_tone', False):
                processed_image = self.skin_enhancer.skin_tone_adjustment(
                    processed_image, landmarks, adjustment=15
                )
            
            self.progress.emit(85)
            
            if self.options.get('eye', False):
                processed_image = self.skin_enhancer.eye_brightening(
                    processed_image, landmarks, brightness_boost=15, sharpness=1.3
                )
            
            if self.options.get('teeth', False):
                processed_image = self.skin_enhancer.teeth_whitening(
                    processed_image, landmarks, whitening_strength=25
                )
            
            self.progress.emit(95)
            
            # 6. Scale landmarks về kích thước gốc nếu cần
            scaled_landmarks = landmarks
            if landmarks is not None and processed_image.shape[:2] != original_shape:
                # Tính scale factor
                current_h, current_w = processed_image.shape[:2]
                original_h, original_w = original_shape
                
                scale_x = original_w / current_w
                scale_y = original_h / current_h
                
                # Scale landmarks
                scaled_landmarks = landmarks.copy()
                scaled_landmarks[:, 0] = landmarks[:, 0] * scale_x  # x coordinates
                scaled_landmarks[:, 1] = landmarks[:, 1] * scale_y  # y coordinates
            
            # 7. Resize ảnh về kích thước gốc nếu cần
            if processed_image.shape[:2] != original_shape:
                processed_image = cv2.resize(
                    processed_image, 
                    (original_shape[1], original_shape[0]),
                    interpolation=cv2.INTER_CUBIC
                )
            
            self.progress.emit(100)
            
            # Emit kết quả với landmarks đã scale
            self.finished.emit(processed_image, scaled_landmarks)
            
        except Exception as e:
            self.error.emit(f"Lỗi xử lý: {str(e)}")

class BeardDetector:
    """
    Lớp phát hiện vùng râu để bảo vệ khỏi xử lý
    """
    
    @staticmethod
    def detect_beard_regions(image, landmarks):
        """
        Phát hiện vùng có râu dựa trên texture và color analysis
        """
        if landmarks is None or len(landmarks) < 468:
            return np.zeros(image.shape[:2], dtype=np.uint8)
        
        # Vùng chin và jaw từ MediaPipe landmarks
        chin_indices = [175, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 397, 288, 361, 323]
        
        if max(chin_indices) >= len(landmarks):
            return np.zeros(image.shape[:2], dtype=np.uint8)
        
        # Tạo mask cho vùng chin
        chin_points = landmarks[chin_indices][:, :2].astype(np.int32)
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [chin_points], 255)
        
        # Mở rộng vùng chin xuống dưới
        h, w = image.shape[:2]
        chin_bottom = np.max(chin_points[:, 1])
        extension_height = int(h * 0.1)  # 10% chiều cao ảnh
        
        # Tạo rectangle mở rộng
        x_min = np.min(chin_points[:, 0])
        x_max = np.max(chin_points[:, 0])
        y_min = chin_bottom
        y_max = min(h, chin_bottom + extension_height)
        
        cv2.rectangle(mask, (x_min, y_min), (x_max, y_max), 255, -1)
        
        # Phân tích texture để detect râu
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Tính variance để detect texture (râu có texture cao)
        kernel = np.ones((5, 5), np.float32) / 25
        mean = cv2.filter2D(gray.astype(np.float32), -1, kernel)
        sqr_mean = cv2.filter2D((gray.astype(np.float32))**2, -1, kernel)
        variance = sqr_mean - mean**2
        
        # Threshold variance cao (có râu)
        _, beard_texture_mask = cv2.threshold(variance, 100, 255, cv2.THRESH_BINARY)
        
        # Kết hợp với chin mask
        beard_mask = cv2.bitwise_and(mask, beard_texture_mask.astype(np.uint8))
        
        # Morphological operations để làm mịn
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        beard_mask = cv2.morphologyEx(beard_mask, cv2.MORPH_CLOSE, kernel)
        beard_mask = cv2.GaussianBlur(beard_mask, (5, 5), 0)
        
        return beard_mask
