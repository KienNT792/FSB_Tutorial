import cv2
import os

# Data file
video_path = 'C:/Users/63200744/Desktop/AI/Udemy/Matering_Python_OpenCV_with_32_Real_world_projects/project/videos/video1.mp4'

def FrameCapture(path):
    if not os.path.exists(path):
        print(f"Video không tồn tại: {path}")
        return
    
    viobj = cv2.VideoCapture(path)
    
    count = 0
    success, image = viobj.read()
    
    while success:
        if image is not None:
            cv2.imwrite(f"Frame{count}.jpg", image)  # Lưu frame
            print(f"Lưu frame {count}")
        else:
            print(f"Frame {count} bị rỗng, bỏ qua.")
        count += 1
        success, image = viobj.read()

if __name__ == '__main__':
    FrameCapture(video_path)