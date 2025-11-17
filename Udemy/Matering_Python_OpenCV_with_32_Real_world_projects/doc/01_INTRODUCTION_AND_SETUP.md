# Giới thiệu và Cài đặt OpenCV

## I. OpenCV là gì?

### 1. Các điểm chính:
- OpenCV (Open Source Computer Vision Library) là một thư viện mã nguồn mở dành cho thị giác máy tính, xử lý ảnh và học máy.
- Ban đầu được phát triển bởi Intel, hiện được duy trì bởi cộng đồng mã nguồn mở.
- Được viết bằng C++ nhưng có các ràng buộc Python (module `cv2`).

### 2. Các ứng dụng của OpenCV:
- Nhận diện khuôn mặt (Face Recognition).
- Phát hiện và theo dõi đối tượng (Object Detection & Tracking).
- Lọc ảnh (Image Filtering).
- Thực tế tăng cường (Augmented Reality).
- Nhận diện ký tự quang học (Optical Character Recognition - OCR).

## II. Cài đặt OpenCV

### 1. Kiểm tra phiên bản Python:
```bash
python --version
```

### 2. Cài đặt OpenCV:
```bash
pip install opencv-contrib-python
```

### 3. Kiểm tra cài đặt OpenCV:
```python
import cv2
print(cv2.__version__)
```

Nếu lệnh trên in ra phiên bản của OpenCV, thì cài đặt đã thành công.

---

## III. Các bước bổ sung (nếu cần):

### 1. Cài đặt thêm thư viện hỗ trợ:
Nếu bạn cần xử lý các định dạng ảnh đặc biệt hoặc sử dụng các tính năng nâng cao, hãy cài đặt thêm:
```bash
pip install numpy matplotlib
```

### 2. Kiểm tra môi trường làm việc:
Đảm bảo rằng bạn đang làm việc trong môi trường ảo (virtual environment) để tránh xung đột thư viện:
```bash
python -m venv opencv_env
source opencv_env/bin/activate  # Trên Linux/Mac
opencv_env\Scripts\activate   # Trên Windows
```

### 3. Tài liệu tham khảo:
- [Tài liệu chính thức OpenCV](https://docs.opencv.org/)
- [Kho GitHub OpenCV](https://github.com/opencv/opencv)

---

## IV. Lưu ý:
- Đảm bảo rằng bạn đã cài đặt Python phiên bản >= 3.6.
- Nếu gặp lỗi trong quá trình cài đặt, hãy kiểm tra lại kết nối mạng hoặc thử sử dụng lệnh:
```bash
pip install --upgrade pip
pip install opencv-contrib-python
```
