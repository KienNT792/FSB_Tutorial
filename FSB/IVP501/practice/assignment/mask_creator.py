import cv2
import numpy as np
from config import FACE_LANDMARKS, IMAGE_PROCESSING_CONFIG

class MaskCreator:
    """
    Lớp tạo mask cho vùng da với forehead expansion
    """
    def __init__(self):
        pass
    
    def create_skin_mask(self, image, landmarks):
        """
        Tạo mặt nạ vùng da với feathering cải tiến và forehead expansion
        """
        h, w = image.shape[:2]
        mask = np.zeros((h, w), dtype=np.uint8)
        
        if landmarks is None:
            return np.ones((h, w), dtype=np.float32) * 0.3
        
        # Tạo mask dựa trên số lượng landmarks
        if len(landmarks) >= 400:  # MediaPipe full landmarks
            mask = self._create_mediapipe_mask(image, landmarks, mask)
        else:  # Synthetic landmarks
            mask = self._create_synthetic_mask(image, landmarks, mask)
        
        # Mở rộng vùng trán cho người hói
        mask = self._expand_forehead_region(image, landmarks, mask)
        
        # Loại bỏ vùng bảo vệ
        mask = self._remove_protected_regions(mask, landmarks)
        
        # Feathering
        return self._apply_feathering(mask)
    
    def _create_mediapipe_mask(self, image, landmarks, mask):
        """
        Tạo mask từ MediaPipe landmarks
        """
        face_oval_indices = FACE_LANDMARKS['face_oval']
        
        if len(landmarks) >= max(face_oval_indices):
            face_points = landmarks[face_oval_indices][:, :2].astype(np.int32)
            cv2.fillPoly(mask, [face_points], 255)
        
        return mask
    
    def _create_synthetic_mask(self, image, landmarks, mask):
        """
        Tạo mask từ synthetic landmarks
        """
        if len(landmarks) >= 17:
            face_outline = landmarks[:17][:, :2].astype(np.int32)
            cv2.fillPoly(mask, [face_outline], 255)
        
        return mask
    
    def _expand_forehead_region(self, image, landmarks, mask):
        """
        Mở rộng vùng trán thông minh cho người hói
        """
        h, w = image.shape[:2]
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return mask
        
        main_contour = max(contours, key=cv2.contourArea)
        x, y, face_w, face_h = cv2.boundingRect(main_contour)
        
        # Phân tích hairline
        hairline_y = self._detect_hairline(image, x, y, face_w, face_h)
        
        if hairline_y is None:
            hairline_y = max(0, y - int(face_h * 0.25))
        
        # Tạo vùng trán mở rộng
        forehead_points = self._create_forehead_polygon(x, y, face_w, face_h, hairline_y)
        
        if forehead_points is not None:
            forehead_mask = np.zeros_like(mask)
            cv2.fillPoly(forehead_mask, [forehead_points], 255)
            mask = cv2.bitwise_or(mask, forehead_mask)
        
        return mask
    
    def _detect_hairline(self, image, x, y, w, h):
        """
        Detect hairline thông minh cho mở rộng trán
        """
        forehead_roi_y = max(0, y - int(h * 0.3))
        forehead_roi = image[forehead_roi_y:y + int(h * 0.4), x:x+w]
        
        if forehead_roi.size == 0:
            return None
        
        gray_forehead = cv2.cvtColor(forehead_roi, cv2.COLOR_BGR2GRAY)
        
        # Edge detection
        edges = cv2.Canny(gray_forehead, 30, 100)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=20, 
                               minLineLength=w//5, maxLineGap=15)
        
        if lines is not None:
            top_line_y = float('inf')
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if abs(y2 - y1) < h * 0.1:
                    line_y = min(y1, y2)
                    if line_y < top_line_y:
                        top_line_y = line_y
            
            if top_line_y != float('inf'):
                return forehead_roi_y + int(top_line_y)
        
        # Texture variance analysis
        variance_profile = []
        step = max(1, gray_forehead.shape[0] // 20)
        for row_idx in range(0, gray_forehead.shape[0] - step, step):
            row_section = gray_forehead[row_idx:row_idx+step, :]
            variance_profile.append(np.var(row_section))
        
        if len(variance_profile) > 3:
            variance_diff = np.diff(variance_profile)
            significant_threshold = np.std(variance_diff) * 1.5
            
            significant_changes = np.where(np.abs(variance_diff) > significant_threshold)[0]
            if len(significant_changes) > 0:
                change_idx = significant_changes[0] * step
                return forehead_roi_y + change_idx
        
        return None
    
    def _create_forehead_polygon(self, x, y, w, h, hairline_y):
        """
        Tạo polygon cho vùng trán mở rộng
        """
        expansion_factor = min(0.4, max(0.15, (y - hairline_y) / h))
        side_expansion = w * 0.1
        
        forehead_points = np.array([
            [x + w * 0.15, y],
            [x + w * 0.85, y],
            [x + w * 0.85 + side_expansion, hairline_y],
            [x + w * 0.5, max(0, hairline_y - h * 0.1)],
            [x + w * 0.15 - side_expansion, hairline_y]
        ], dtype=np.int32)
        
        return forehead_points
    
    def _remove_protected_regions(self, mask, landmarks):
        """
        Loại bỏ vùng mắt, miệng khỏi mask
        """
        if landmarks is None:
            return mask
        
        if len(landmarks) >= 400:  # MediaPipe landmarks
            # Eyes and mouth
            for region_name in ['left_eye', 'right_eye', 'mouth']:
                indices = FACE_LANDMARKS[region_name]
                if len(landmarks) > max(indices):
                    points = landmarks[indices][:, :2].astype(np.int32)
                    cv2.fillPoly(mask, [points], 0)
        
        else:  # Synthetic landmarks
            if len(landmarks) > 30:
                left_eye = landmarks[17:23][:, :2].astype(np.int32)
                right_eye = landmarks[23:29][:, :2].astype(np.int32)
                cv2.fillPoly(mask, [left_eye], 0)
                cv2.fillPoly(mask, [right_eye], 0)
            
            if len(landmarks) > 40:
                mouth = landmarks[38:52][:, :2].astype(np.int32)
                cv2.fillPoly(mask, [mouth], 0)
        
        return mask
    
    def _apply_feathering(self, mask):
        """
        Áp dụng feathering cho mask
        """
        mask_float = mask.astype(np.float32) / 255.0
        kernel_size = IMAGE_PROCESSING_CONFIG['morph_kernel_size']
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
        mask_float = cv2.erode(mask_float, kernel, 
                              iterations=IMAGE_PROCESSING_CONFIG['erosion_iterations'])
        mask_float = cv2.GaussianBlur(mask_float, IMAGE_PROCESSING_CONFIG['gaussian_blur_kernel'], 0)
        
        return mask_float
