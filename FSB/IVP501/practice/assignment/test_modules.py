"""
Script demo để test các module đã tách
"""

import cv2
import numpy as np
from face_detector import FaceDetector
from mask_creator import MaskCreator
from image_processor import ImageProcessor, SkinEnhancer, LandmarksVisualizer

def test_modules():
    """
    Test các module cơ bản
    """
    print("🧪 Testing modules...")
    
    # Test 1: Face Detector
    print("\n1️⃣ Testing FaceDetector...")
    detector = FaceDetector()
    print("   ✅ FaceDetector initialized")
    
    # Test 2: Mask Creator
    print("\n2️⃣ Testing MaskCreator...")
    mask_creator = MaskCreator()
    print("   ✅ MaskCreator initialized")
    
    # Test 3: Image Processor
    print("\n3️⃣ Testing ImageProcessor...")
    processor = ImageProcessor()
    print("   ✅ ImageProcessor initialized")
    
    # Test 4: Skin Enhancer
    print("\n4️⃣ Testing SkinEnhancer...")
    enhancer = SkinEnhancer()
    print("   ✅ SkinEnhancer initialized")
    
    # Test 5: Landmarks Visualizer
    print("\n5️⃣ Testing LandmarksVisualizer...")
    visualizer = LandmarksVisualizer()
    print("   ✅ LandmarksVisualizer initialized")
    
    print("\n✨ All modules initialized successfully!")
    print("\n📋 Module Summary:")
    print("   • face_detector.py - FaceDetector")
    print("   • mask_creator.py - MaskCreator")
    print("   • image_processor.py - ImageProcessor, SkinEnhancer, LandmarksVisualizer")
    print("   • processing_thread.py - ProcessingThread")
    print("   • ui_components.py - UIComponents")
    print("   • config.py - Configuration")
    print("   • main.py - Main Application")

if __name__ == "__main__":
    test_modules()
