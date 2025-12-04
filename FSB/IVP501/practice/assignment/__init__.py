# Skin Processor Application Package
# Advanced AI-powered skin processing desktop application

__version__ = "2.0.0"
__author__ = "AI Assistant"
__description__ = "Desktop application for AI-powered skin processing with modular architecture"

# Module imports for easy access
from .face_detector import FaceDetector
from .mask_creator import MaskCreator  
from .image_processor import ImageProcessor, SkinEnhancer
from .processing_thread import ProcessingThread
from .ui_components import UIComponents
from . import config

__all__ = [
    'FaceDetector',
    'MaskCreator', 
    'ImageProcessor',
    'SkinEnhancer',
    'ProcessingThread',
    'UIComponents',
    'config'
]
