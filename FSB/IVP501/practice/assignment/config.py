# Configuration settings for the Skin Processor application

# MediaPipe settings
MEDIAPIPE_CONFIG = {
    'static_image_mode': True,
    'max_num_faces': 1,
    'refine_landmarks': True,
    'min_detection_confidence': 0.3,
    'min_tracking_confidence': 0.3
}

# Image processing settings
IMAGE_PROCESSING_CONFIG = {
    'max_size': 1024,
    'gaussian_blur_kernel': (21, 21),
    'morph_kernel_size': (5, 5),
    'erosion_iterations': 2,
    'bilateral_iterations': 2
}

# GUI settings
GUI_CONFIG = {
    'window_title': 'Ứng dụng Xử lý Da - Phiên bản Nâng cao',
    'window_geometry': (100, 100, 1400, 900),
    'control_panel_width': 280,
    'splitter_sizes': [300, 1100],
    'info_text_height': 150,
    'min_image_size': (500, 400)
}

# Default values
DEFAULT_VALUES = {
    'strength': 70,
    'method': 'guided',
    'brightness_boost': 15,
    'sharpness': 1.3,
    'whitening_strength': 25,
    'wrinkle_strength': 0.6,
    'blemish_strength': 0.8
}

# Face landmarks indices
FACE_LANDMARKS = {
    'face_oval': [
        10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
        397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
        172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109
    ],
    'left_eye': [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246],
    'right_eye': [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398],
    'mouth': [61, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318],
    'teeth_detection': [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]
}

# Color ranges
COLOR_RANGES = {
    'teeth_lower': [0, 0, 150],
    'teeth_upper': [180, 50, 255]
}
