# Các Hàm Cơ Bản (Essential Functions) trong OpenCV

## Mục lục
1. [Đọc và ghi ảnh/video](#1-đọc-và-ghi-ảnhvideo)
2. [Hiển thị ảnh/video](#2-hiển-thị-ảnhvideo)
3. [Xử lý ảnh cơ bản](#3-xử-lý-ảnh-cơ-bản)
4. [Vẽ hình và văn bản](#4-vẽ-hình-và-văn-bản)
5. [Phát hiện cạnh và đường](#5-phát-hiện-cạnh-và-đường)
6. [Biến đổi hình học](#6-biến-đổi-hình-học)
7. [Xử lý nâng cao](#7-xử-lý-nâng-cao)

---

## 1. Đọc và ghi ảnh/video

### Đọc ảnh
```python
cv.imread(path, flag)
```
- **Mô tả**: Đọc ảnh từ file.
- **Tham số**:
  - `path`: Đường dẫn đến file ảnh.
  - `flag`: Cách đọc ảnh:
    - `cv.IMREAD_COLOR`: Đọc ảnh màu (mặc định).
    - `cv.IMREAD_GRAYSCALE`: Đọc ảnh ở chế độ grayscale.
    - `cv.IMREAD_UNCHANGED`: Đọc ảnh bao gồm cả kênh alpha (nếu có).
- **Trả về**: Mảng NumPy đại diện cho ảnh.

### Ghi ảnh
```python
cv.imwrite(filename, image)
```
- **Mô tả**: Ghi ảnh vào file.
- **Tham số**:
  - `filename`: Tên file để lưu ảnh.
  - `image`: Mảng NumPy đại diện cho ảnh.

### Đọc video
```python
cv.VideoCapture(path)
```
- **Mô tả**: Đọc video từ file hoặc webcam.
- **Tham số**:
  - `path`: Đường dẫn đến file video hoặc số `0` để mở webcam.
- **Trả về**: Đối tượng `VideoCapture`.

### Ghi video
```python
cv.VideoWriter()
```
- **Mô tả**: Ghi video vào file.

---

## 2. Hiển thị ảnh/video

### Hiển thị ảnh
```python
cv.imshow(window_name, image)
```
- **Mô tả**: Hiển thị ảnh trong cửa sổ.
- **Tham số**:
  - `window_name`: Tên cửa sổ.
  - `image`: Mảng NumPy đại diện cho ảnh.

### Chờ phím nhấn
```python
cv.waitKey(delay)
```
- **Mô tả**: Chờ trong `delay` milliseconds để người dùng nhấn phím.
- **Tham số**:
  - `delay`: Thời gian chờ (ms). Nếu `delay=0`, chờ vô hạn.

### Đóng cửa sổ
```python
cv.destroyAllWindows()
```
- **Mô tả**: Đóng tất cả các cửa sổ OpenCV.

---

## 3. Xử lý ảnh cơ bản

### Thay đổi kích thước ảnh
```python
cv.resize(image, dsize)
```
- **Mô tả**: Thay đổi kích thước ảnh.
- **Tham số**:
  - `image`: Ảnh đầu vào.
  - `dsize`: Kích thước mới (width, height).

### Chuyển đổi không gian màu
```python
cv.cvtColor(image, code)
```
- **Mô tả**: Chuyển đổi không gian màu (ví dụ: BGR <-> Grayscale).
- **Tham số**:
  - `code`: Mã chuyển đổi (ví dụ: `cv.COLOR_BGR2GRAY`).

### Lật ảnh
```python
cv.flip(image, flipCode)
```
- **Mô tả**: Lật ảnh theo chiều ngang, dọc, hoặc cả hai.
- **Tham số**:
  - `flipCode`: 
    - `0`: Lật theo chiều dọc.
    - `1`: Lật theo chiều ngang.
    - `-1`: Lật cả hai chiều.

### Làm mờ ảnh
```python
cv.GaussianBlur(image, ksize, sigmaX)
```
- **Mô tả**: Làm mờ ảnh bằng Gaussian Blur.
- **Tham số**:
  - `ksize`: Kích thước kernel (ví dụ: `(5, 5)`).
  - `sigmaX`: Độ lệch chuẩn theo trục X.

---

## 4. Vẽ hình và văn bản

### Vẽ đường thẳng
```python
cv.line(image, pt1, pt2, color, thickness)
```
- **Mô tả**: Vẽ đường thẳng.
- **Tham số**:
  - `pt1`: Điểm bắt đầu (x1, y1).
  - `pt2`: Điểm kết thúc (x2, y2).
  - `color`: Màu của đường thẳng (BGR).
  - `thickness`: Độ dày của đường thẳng.

### Vẽ hình chữ nhật
```python
cv.rectangle(image, pt1, pt2, color, thickness)
```
- **Mô tả**: Vẽ hình chữ nhật.
- **Tham số**:
  - `image`: Ảnh đầu vào.
  - `pt1`: Góc trên bên trái của hình chữ nhật (x1, y1).
  - `pt2`: Góc dưới bên phải của hình chữ nhật (x2, y2).
  - `color`: Màu của hình chữ nhật (BGR).
  - `thickness`: 
    - Số dương: Độ dày của viền.
    - `cv.FILLED` hoặc `-1`: Tô đầy hình chữ nhật.

### Vẽ hình tròn
```python
cv.circle(image, center, radius, color, thickness)
```
- **Mô tả**: Vẽ hình tròn.
- **Tham số**:
  - `image`: Ảnh đầu vào.
  - `center`: Tọa độ tâm của hình tròn (x, y).
  - `radius`: Bán kính của hình tròn.
  - `color`: Màu của hình tròn (BGR).
  - `thickness`: 
    - Số dương: Độ dày của viền.
    - `cv.FILLED` hoặc `-1`: Tô đầy hình tròn.

### Viết chữ
```python
cv.putText(image, text, org, font, fontScale, color, thickness)
```
- **Mô tả**: Vẽ văn bản lên ảnh.
- **Tham số**:
  - `image`: Ảnh đầu vào.
  - `text`: Chuỗi văn bản cần vẽ.
  - `org`: Tọa độ góc dưới bên trái của chữ (x, y).
  - `font`: Kiểu chữ (ví dụ: `cv.FONT_HERSHEY_SIMPLEX`).
  - `fontScale`: Kích thước chữ.
  - `color`: Màu của chữ (BGR).
  - `thickness`: Độ dày của chữ.

---

## 5. Phát hiện cạnh và đường

### Phát hiện cạnh
```python
cv.Canny(image, threshold1, threshold2)
```
- **Mô tả**: Phát hiện cạnh bằng thuật toán Canny.

### Phát hiện đường thẳng
```python
cv.HoughLines(image, rho, theta, threshold)
```
- **Mô tả**: Phát hiện đường thẳng bằng Hough Transform.

### Phát hiện hình tròn
```python
cv.HoughCircles(image, method, dp, minDist)
```
- **Mô tả**: Phát hiện hình tròn bằng Hough Transform.
- **Tham số**:
  - `image`: Ảnh đầu vào (ảnh grayscale).
  - `method`: Phương pháp phát hiện (thường là `cv.HOUGH_GRADIENT`).
  - `dp`: Tỉ lệ nghịch giữa độ phân giải ảnh và độ phân giải bộ tích lũy.
  - `minDist`: Khoảng cách tối thiểu giữa các tâm hình tròn được phát hiện.
  - Các tham số khác (nếu có): `param1`, `param2` để điều chỉnh thuật toán.

---

## 6. Biến đổi hình học

### Biến đổi affine
```python
cv.warpAffine(image, M, dsize)
```
- **Mô tả**: Áp dụng biến đổi affine.
- **Tham số**:
  - `image`: Ảnh đầu vào.
  - `M`: Ma trận biến đổi affine (2x3).
  - `dsize`: Kích thước ảnh đầu ra (width, height).

### Biến đổi phối cảnh
```python
cv.warpPerspective(image, M, dsize)
```
- **Mô tả**: Áp dụng biến đổi phối cảnh.
- **Tham số**:
  - `image`: Ảnh đầu vào.
  - `M`: Ma trận biến đổi phối cảnh (3x3).
  - `dsize`: Kích thước ảnh đầu ra (width, height).

---

## 7. Xử lý nâng cao

### Giãn ảnh
```python
cv.dilate(image, kernel)
```
- **Mô tả**: Giãn ảnh (dilate).
- **Tham số**:
  - `image`: Ảnh đầu vào.
  - `kernel`: Kernel (ma trận) để áp dụng phép giãn.

### Co ảnh
```python
cv.erode(image, kernel)
```
- **Mô tả**: Co ảnh (erode).
- **Tham số**:
  - `image`: Ảnh đầu vào.
  - `kernel`: Kernel (ma trận) để áp dụng phép co.

### Cân bằng histogram
```python
cv.equalizeHist(image)
```
- **Mô tả**: Cân bằng histogram của ảnh grayscale.