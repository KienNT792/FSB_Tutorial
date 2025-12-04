# Image Processing Filters and Enhancement Algorithms

import cv2
import numpy as np
from config import IMAGE_PROCESSING_CONFIG, FACE_LANDMARKS

class ImageProcessor:
    """
    Lớp xử lý ảnh với các thuật toán filter và enhancement
    """
    
    def __init__(self):
        pass
    
    def preprocess_image(self, image, max_size=None):
        """
        Tiền xử lý ảnh: resize và chuẩn hóa
        """
        if max_size is None:
            max_size = IMAGE_PROCESSING_CONFIG['max_size']
            
        # Lưu kích thước gốc
        original_shape = image.shape[:2]
        
        # Resize nếu ảnh quá lớn
        height, width = image.shape[:2]
        if max(height, width) > max_size:
            scale = max_size / max(height, width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Chuyển BGR sang RGB cho MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        return rgb_image, original_shape
    
    def apply_bilateral_filter(self, image, mask, strength=0.7):
        """
        Áp dụng Bilateral Filter với mask
        """
        # Tạo ảnh làm mịn
        iterations = IMAGE_PROCESSING_CONFIG['bilateral_iterations']
        smoothed = image.copy()
        
        for _ in range(iterations):
            smoothed = cv2.bilateralFilter(smoothed, 15, 80, 80)
        
        # Blend với mask
        mask_3d = np.stack([mask] * 3, axis=-1)
        result = image * (1 - mask_3d * strength) + smoothed * (mask_3d * strength)
        
        return result.astype(np.uint8)
    
    def apply_guided_filter(self, image, mask, strength=0.7):
        """
        Guided Filter implementation (đơn giản hóa)
        """
        # Chuyển sang LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Áp dụng guided filter trên L channel
        l_float = l.astype(np.float32) / 255.0
        
        # Box filter approximation
        kernel_size = 15
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
        
        # Mean of I and correlation
        mean_I = cv2.filter2D(l_float, -1, kernel)
        corr_I = cv2.filter2D(l_float * l_float, -1, kernel)
        
        # Variance
        var_I = corr_I - mean_I * mean_I
        
        # Parameters
        eps = 0.04
        
        # Linear coefficients
        a_coeff = var_I / (var_I + eps)
        b_coeff = mean_I - a_coeff * mean_I
        
        # Filter coefficients
        mean_a = cv2.filter2D(a_coeff, -1, kernel)
        mean_b = cv2.filter2D(b_coeff, -1, kernel)
        
        # Output
        l_filtered = mean_a * l_float + mean_b
        l_filtered = np.clip(l_filtered * 255, 0, 255).astype(np.uint8)
        
        # Merge back
        lab_filtered = cv2.merge([l_filtered, a, b])
        result = cv2.cvtColor(lab_filtered, cv2.COLOR_LAB2BGR)
        
        # Apply mask
        mask_3d = np.stack([mask] * 3, axis=-1)
        result = image * (1 - mask_3d * strength) + result * (mask_3d * strength)
        
        return result.astype(np.uint8)
    
    def apply_edge_preserving_filter(self, image, mask, strength=0.7):
        """
        Edge-preserving filter
        """
        # Sử dụng edge-preserving filter của OpenCV
        smoothed = cv2.edgePreservingFilter(image, flags=2, sigma_s=150, sigma_r=0.4)
        
        # Blend với mask
        mask_3d = np.stack([mask] * 3, axis=-1)
        result = image * (1 - mask_3d * strength) + smoothed * (mask_3d * strength)
        
        return result.astype(np.uint8)
    
    def apply_advanced_blend(self, image, mask, strength=0.7):
        """
        Advanced blending với multiple techniques
        """
        # 1. Bilateral filter
        bilateral = cv2.bilateralFilter(image, 15, 80, 80)
        
        # 2. Gaussian blur với large kernel
        gaussian = cv2.GaussianBlur(image, (21, 21), 0)
        
        # 3. Edge-preserving
        edge_preserve = cv2.edgePreservingFilter(image, flags=1, sigma_s=100, sigma_r=0.2)
        
        # 4. Weighted combination
        combined = (bilateral * 0.4 + gaussian * 0.3 + edge_preserve * 0.3).astype(np.uint8)
        
        # 5. Apply mask
        mask_3d = np.stack([mask] * 3, axis=-1)
        result = image * (1 - mask_3d * strength) + combined * (mask_3d * strength)
        
        return result.astype(np.uint8)

class SkinEnhancer:
    """
    Lớp cải thiện da với các thuật toán nâng cao
    """
    
    def __init__(self):
        pass
    
    def blemish_removal(self, image, landmarks, strength=0.8):
        """
        Loại bỏ mụn, tàn nhang bằng Inpainting-like approach
        """
        if landmarks is None:
            return image
        
        result = image.copy()
        
        # Chuyển sang LAB để phân tích da tốt hơn
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l_channel = lab[:, :, 0]
        
        # Detect blemishes bằng cách tìm điểm sáng/tối bất thường
        # Gaussian blur để tìm nền
        blurred = cv2.GaussianBlur(l_channel, (15, 15), 0)
        
        # Tìm khác biệt
        diff = cv2.absdiff(l_channel, blurred)
        
        # Threshold để tìm blemishes
        _, blemish_mask = cv2.threshold(diff, 15, 255, cv2.THRESH_BINARY)
        
        # Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        blemish_mask = cv2.morphologyEx(blemish_mask, cv2.MORPH_OPEN, kernel)
        blemish_mask = cv2.dilate(blemish_mask, kernel, iterations=1)
        
        # Inpainting
        if cv2.countNonZero(blemish_mask) > 0:
            inpainted = cv2.inpaint(result, blemish_mask, 3, cv2.INPAINT_TELEA)
            
            # Blend với cường độ
            mask_normalized = blemish_mask.astype(np.float32) / 255.0 * strength
            mask_3d = np.stack([mask_normalized] * 3, axis=-1)
            
            result = result * (1 - mask_3d) + inpainted * mask_3d
        
        return result.astype(np.uint8)
    
    def wrinkle_reduction(self, image, landmarks, strength=0.6):
        """
        Giảm nếp nhăn bằng selective smoothing
        """
        if landmarks is None:
            return image
        
        result = image.copy()
        
        # Chuyển sang grayscale để detect wrinkles
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect edges (wrinkles are often edges)
        edges = cv2.Canny(gray, 50, 150)
        
        # Dilate để mở rộng vùng wrinkle
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        wrinkle_mask = cv2.dilate(edges, kernel, iterations=2)
        
        # Gaussian blur để làm mịn wrinkles
        smoothed = cv2.GaussianBlur(result, (7, 7), 0)
        
        # Apply selective smoothing
        mask_normalized = wrinkle_mask.astype(np.float32) / 255.0 * strength
        mask_3d = np.stack([mask_normalized] * 3, axis=-1)
        
        result = result * (1 - mask_3d) + smoothed * mask_3d
        
        return result.astype(np.uint8)
    
    def skin_tone_adjustment(self, image, landmarks, adjustment=15):
        """
        Điều chỉnh màu da
        """
        if landmarks is None:
            return image
        
        # Chuyển sang LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Tăng brightness (L channel) 
        l = l.astype(np.float32)
        l = l + adjustment
        l = np.clip(l, 0, 255).astype(np.uint8)
        
        # Giảm red tint (a channel)
        a = a.astype(np.float32)
        a = a * 0.95  # Slight reduction
        a = np.clip(a, 0, 255).astype(np.uint8)
        
        # Merge và convert back
        lab_adjusted = cv2.merge([l, a, b])
        result = cv2.cvtColor(lab_adjusted, cv2.COLOR_LAB2BGR)
        
        return result
    
    def eye_brightening(self, image, landmarks, brightness_boost=15, sharpness=1.3):
        """
        Làm sáng vùng mắt
        """
        if landmarks is None or len(landmarks) < 468:
            return image
        
        result = image.copy()
        
        # Vùng mắt từ MediaPipe landmarks
        left_eye_indices = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        right_eye_indices = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        
        eye_regions = [left_eye_indices, right_eye_indices]
        
        for eye_indices in eye_regions:
            if max(eye_indices) >= len(landmarks):
                continue
                
            # Lấy điểm mắt
            eye_points = landmarks[eye_indices][:, :2].astype(np.int32)
            
            # Tạo ROI cho mắt
            x, y, w, h = cv2.boundingRect(eye_points)
            
            # Mở rộng ROI
            padding = 10
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(image.shape[1] - x, w + 2 * padding)
            h = min(image.shape[0] - y, h + 2 * padding)
            
            # Extract ROI
            eye_roi = result[y:y+h, x:x+w].copy()
            
            # Tăng độ sáng
            eye_roi = cv2.convertScaleAbs(eye_roi, alpha=1.0, beta=brightness_boost)
            
            # Tăng độ sắc nét
            if sharpness > 1.0:
                blurred = cv2.GaussianBlur(eye_roi, (0, 0), 3)
                eye_roi = cv2.addWeighted(eye_roi, sharpness, blurred, 1 - sharpness, 0)
            
            # Đặt lại vào ảnh
            result[y:y+h, x:x+w] = eye_roi
        
        return result
    
    def teeth_whitening(self, image, landmarks, whitening_strength=30):
        """
        Làm trắng răng
        """
        if landmarks is None or len(landmarks) < 468:
            return image
        
        # Vùng môi để detect răng
        mouth_indices = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]
        
        if max(mouth_indices) >= len(landmarks):
            return image
        
        mouth_points = landmarks[mouth_indices][:, :2].astype(np.int32)
        
        # Tạo mask cho vùng miệng
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [mouth_points], 255)
        
        # Chuyển sang HSV để detect răng
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Threshold để tìm vùng sáng (răng)
        lower_white = np.array([0, 0, 150])
        upper_white = np.array([180, 50, 255])
        teeth_mask = cv2.inRange(hsv, lower_white, upper_white)
        
        # Kết hợp với mouth mask
        teeth_mask = cv2.bitwise_and(teeth_mask, mask)
        
        # Làm mịn mask
        teeth_mask = cv2.GaussianBlur(teeth_mask, (7, 7), 0)
        teeth_mask = teeth_mask.astype(np.float32) / 255.0
        
        # Tăng brightness và giảm saturation
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Tăng L channel
        l = l.astype(np.float32)
        l = l + (whitening_strength * teeth_mask)
        l = np.clip(l, 0, 255).astype(np.uint8)
        
        # Giảm a, b (desaturate)
        a = a.astype(np.float32)
        a = a * (1 - teeth_mask * 0.3)
        a = np.clip(a, 0, 255).astype(np.uint8)
        
        b = b.astype(np.float32)
        b = b * (1 - teeth_mask * 0.3)
        b = np.clip(b, 0, 255).astype(np.uint8)
        
        # Merge
        whitened_lab = cv2.merge([l, a, b])
        result = cv2.cvtColor(whitened_lab, cv2.COLOR_LAB2BGR)
        
        return result

class LandmarksVisualizer:
    """
    Lớp để vẽ và hiển thị landmarks trên ảnh
    """
    
    @staticmethod
    def draw_landmarks(image, landmarks, show_connections=True, show_indices=False):
        """
        Vẽ landmarks lên ảnh
        
        Args:
            image: Ảnh gốc
            landmarks: Mảng landmarks numpy (N, 3) hoặc (N, 2)
            show_connections: Có vẽ đường nối không
            show_indices: Có hiển thị số thứ tự không
            
        Returns:
            Ảnh đã vẽ landmarks
        """
        if landmarks is None:
            # Return image với text thông báo
            result = image.copy()
            h, w = result.shape[:2]
            cv2.putText(result, "No landmarks detected", 
                       (w//4, h//2), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (0, 0, 255), 2)
            return result
        
        result = image.copy()
        
        # Vẽ connections nếu có đủ landmarks (MediaPipe format)
        if show_connections and len(landmarks) >= 468:
            result = LandmarksVisualizer._draw_face_mesh_connections(result, landmarks)
        
        # Vẽ các điểm landmarks
        for idx, landmark in enumerate(landmarks):
            x, y = int(landmark[0]), int(landmark[1])
            
            # Màu sắc theo vùng
            if len(landmarks) >= 468:  # MediaPipe landmarks
                color = LandmarksVisualizer._get_landmark_color(idx)
            else:
                color = (0, 255, 0)  # Green cho synthetic landmarks
            
            # Vẽ điểm
            cv2.circle(result, (x, y), 2, color, -1)
            
            # Vẽ số thứ tự nếu cần
            if show_indices and idx % 10 == 0:  # Chỉ hiển thị mỗi 10 điểm
                cv2.putText(result, str(idx), (x+3, y-3), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
        
        # Thêm legend
        result = LandmarksVisualizer._add_legend(result, len(landmarks))
        
        return result
    
    @staticmethod
    def _get_landmark_color(idx):
        """
        Lấy màu sắc cho từng vùng landmarks
        """
        # Face outline
        if idx in FACE_LANDMARKS.get('face_oval', []):
            return (255, 200, 0)  # Cyan
        # Left eye
        elif idx in FACE_LANDMARKS.get('left_eye', []):
            return (0, 255, 255)  # Yellow
        # Right eye
        elif idx in FACE_LANDMARKS.get('right_eye', []):
            return (0, 255, 255)  # Yellow
        # Mouth
        elif idx in FACE_LANDMARKS.get('mouth', []):
            return (255, 0, 255)  # Magenta
        # Nose
        else:
            return (0, 255, 0)  # Green
    
    @staticmethod
    def _draw_face_mesh_connections(image, landmarks):
        """
        Vẽ các đường nối giữa landmarks (face mesh)
        """
        # Các connections chính cho face mesh
        connections = [
            # Face oval
            FACE_LANDMARKS.get('face_oval', []),
            # Left eye
            FACE_LANDMARKS.get('left_eye', []),
            # Right eye
            FACE_LANDMARKS.get('right_eye', []),
            # Mouth outer
            FACE_LANDMARKS.get('mouth', [])
        ]
        
        # Vẽ các connections
        for connection_group in connections:
            if not connection_group:
                continue
                
            for i in range(len(connection_group)):
                start_idx = connection_group[i]
                end_idx = connection_group[(i + 1) % len(connection_group)]
                
                if start_idx < len(landmarks) and end_idx < len(landmarks):
                    start_point = (int(landmarks[start_idx][0]), int(landmarks[start_idx][1]))
                    end_point = (int(landmarks[end_idx][0]), int(landmarks[end_idx][1]))
                    
                    cv2.line(image, start_point, end_point, (100, 200, 100), 1)
        
        return image
    
    @staticmethod
    def _add_legend(image, num_landmarks):
        """
        Thêm legend vào ảnh
        """
        h, w = image.shape[:2]
        
        # Background cho legend
        legend_h = 100
        legend_w = 200
        overlay = image.copy()
        cv2.rectangle(overlay, (10, 10), (10 + legend_w, 10 + legend_h), 
                     (255, 255, 255), -1)
        image = cv2.addWeighted(overlay, 0.7, image, 0.3, 0)
        
        # Text
        y_offset = 30
        cv2.putText(image, f"Landmarks: {num_landmarks}", 
                   (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.5, (0, 0, 0), 1)
        
        # Legend colors
        if num_landmarks >= 468:
            colors = [
                ((255, 200, 0), "Face Oval"),
                ((0, 255, 255), "Eyes"),
                ((255, 0, 255), "Mouth"),
                ((0, 255, 0), "Nose")
            ]
            
            for i, (color, label) in enumerate(colors):
                y_pos = y_offset + 20 + i * 15
                cv2.circle(image, (25, y_pos - 3), 4, color, -1)
                cv2.putText(image, label, (35, y_pos), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        
        return image
