# Đọc và Hiển thị Ảnh và Video bằng OpenCV

## 1. Đọc và hiển thị ảnh

### Mô tả:
- Để đọc ảnh từ file, sử dụng hàm `cv.imread()`.
- Để hiển thị ảnh, sử dụng hàm `cv.imshow()`.
- Để chờ người dùng nhấn phím và đóng cửa sổ, sử dụng `cv.waitKey()` và `cv.destroyAllWindows()`.

### Code mẫu:
```python
import cv2 as cv  # Import thư viện OpenCV

# Đọc ảnh từ file
image = cv.imread('path_to_image.jpg')  # Đường dẫn đến file ảnh

# Kiểm tra nếu ảnh không được tải thành công
if image is None:
    print("Không thể đọc ảnh. Kiểm tra đường dẫn file.")
    exit()

# Hiển thị ảnh trong cửa sổ
cv.imshow('Hiển thị ảnh', image)  # 'Hiển thị ảnh' là tên cửa sổ

# Chờ người dùng nhấn phím bất kỳ
cv.waitKey(0)  # 0 nghĩa là chờ vô hạn

# Đóng tất cả các cửa sổ
cv.destroyAllWindows()
```

### Giải thích các hàm:
- `cv.imread(path)`: Đọc ảnh từ đường dẫn `path`. Trả về một mảng NumPy đại diện cho ảnh.
- `cv.imshow(window_name, image)`: Hiển thị ảnh trong cửa sổ có tên `window_name`.
- `cv.waitKey(delay)`: Chờ trong `delay` milliseconds để người dùng nhấn phím. Nếu `delay=0`, chờ vô hạn.
- `cv.destroyAllWindows()`: Đóng tất cả các cửa sổ OpenCV.

---

## 2. Đọc và hiển thị video

### Mô tả:
- Để đọc video từ file, sử dụng `cv.VideoCapture()`.
- Để hiển thị từng frame của video, sử dụng `cv.imshow()` trong vòng lặp.
- Để dừng video, sử dụng `cv.waitKey()` để kiểm tra phím nhấn.

### Code mẫu:
```python
import cv2 as cv  # Import thư viện OpenCV

# Đọc video từ file
capture = cv.VideoCapture('path_to_video.mp4')  # Đường dẫn đến file video

# Kiểm tra nếu video không được tải thành công
if not capture.isOpened():
    print("Không thể mở video. Kiểm tra đường dẫn file.")
    exit()

# Vòng lặp để đọc từng frame
while True:
    isTrue, frame = capture.read()  # Đọc frame tiếp theo

    # Kiểm tra nếu không còn frame nào
    if not isTrue:
        print("Đã phát hết video.")
        break

    # Hiển thị frame hiện tại
    cv.imshow('Hiển thị video', frame)

    # Chờ 20ms và kiểm tra nếu phím 'q' được nhấn để thoát
    if cv.waitKey(20) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
capture.release()
cv.destroyAllWindows()
```

### Giải thích các hàm:
- `cv.VideoCapture(path)`: Mở file video từ đường dẫn `path`. Trả về đối tượng `VideoCapture`.
- `capture.read()`: Đọc frame tiếp theo từ video. Trả về:
  - `isTrue`: `True` nếu đọc thành công, `False` nếu hết video.
  - `frame`: Dữ liệu hình ảnh của frame hiện tại.
- `capture.isOpened()`: Kiểm tra nếu video được mở thành công.
- `capture.release()`: Giải phóng tài nguyên liên quan đến video.

---

## 3. Lưu ý:
- Đảm bảo đường dẫn đến file ảnh hoặc video là chính xác.
- Nếu sử dụng webcam, thay đường dẫn file bằng số `0`:
  ```python
  capture = cv.VideoCapture(0)  # Mở webcam mặc định
  ```
- Để xử lý video lớn, bạn có thể giảm kích thước frame bằng cách sử dụng `cv.resize()`:
  ```python
  frame = cv.resize(frame, (width, height))
  ```