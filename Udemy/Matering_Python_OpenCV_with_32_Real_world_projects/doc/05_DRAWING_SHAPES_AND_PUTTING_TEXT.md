# OpenCV Notes

## 1. OpenCV hỗ trợ ảnh 1 kênh (grayscale), 3 kênh (RGB) và 4 kênh (RGB + Alpha)

### a. Ảnh 1 kênh (Grayscale)
- **Số kênh**: 1 
- **Ý nghĩa**: Ảnh đen trắng, mỗi pixel chỉ có giá trị cường độ sáng từ 0 (đen) đến 255 (trắng).
- **Ví dụ**: 
  ```python
  blank = np.zeros((500, 500), dtype='uint8')  # Tạo ảnh grayscale đen
  ```

### b. Ảnh 3 kênh (BGR - Màu)
- **Số kênh**: 3
- **Ý nghĩa**: Ảnh màu với 3 kênh: Blue (B), Green (G), Red (R).
- **Ví dụ**:
  ```python
  blank = np.zeros((500, 500, 3), dtype='uint8')  # Ảnh màu BGR
  ```

### c. Ảnh 4 kênh (BGR - Màu + Alpha)
- **Số kênh**: 4
- **Ý nghĩa**: Ảnh màu với 4 kênh: Blue (B), Green (G), Red (R), và Alpha (A) - kênh trong suốt (transparency).
- **Ví dụ**:
  ```python
  blank = np.zeros((500, 500, 4), dtype='uint8')  # Ảnh BGRA
  ```

---

## 2. Cách vẽ các hình trong ảnh bằng OpenCV

### a. Đường thẳng (Line)
```python
cv.line(IMAGE, (x1, y1), (x2, y2), color, thickness)
```
- **(x1, y1)**: Điểm bắt đầu của đường thẳng.
- **(x2, y2)**: Điểm kết thúc của đường thẳng.
- **color**: Màu của đường thẳng (BGR).
- **thickness**: Độ dày của đường thẳng.
- **Ví dụ**:
  ```python
  cv.line(blank, (50, 50), (450, 450), (255, 0, 0), 5)  # Đường thẳng màu xanh dương
  ```

### b. Hình chữ nhật (Rectangle)
```python
cv.rectangle(IMAGE, (x1, y1), (x2, y2), color, thickness)
```
- **(x1, y1)**: Góc trên bên trái của hình chữ nhật.
- **(x2, y2)**: Góc dưới bên phải của hình chữ nhật.
- **color**: Màu của hình chữ nhật (BGR).
- **thickness**: 
  - Số dương: Độ dày của viền.
  - `cv.FILLED` hoặc `-1`: Tô đầy hình chữ nhật.
- **Ví dụ**:
  ```python
  cv.rectangle(blank, (100, 100), (300, 300), (0, 255, 0), thickness=cv.FILLED)  # Hình chữ nhật màu xanh lá
  ```

### c. Hình tròn (Circle)
```python
cv.circle(IMAGE, center, radius, color, thickness)
```
- **center**: Tọa độ tâm của hình tròn (x, y).
- **radius**: Bán kính hình tròn.
- **color**: Màu của hình tròn (BGR).
- **thickness**: 
  - Số dương: Độ dày của viền.
  - `cv.FILLED` hoặc `-1`: Tô đầy hình tròn.
- **Ví dụ**:
  ```python
  cv.circle(blank, (250, 250), 100, (0, 0, 255), thickness=3)  # Hình tròn màu đỏ
  ```

### d. Hình elip (Ellipse)
```python
cv.ellipse(IMAGE, center, axes, angle, startAngle, endAngle, color, thickness)
```
- **center**: Tọa độ tâm của hình elip (x, y).
- **axes**: Kích thước của hình elip (bán trục lớn, bán trục nhỏ).
- **angle**: Góc xoay của hình elip (tính theo độ).
- **startAngle**: Góc bắt đầu (tính từ trục x dương).
- **endAngle**: Góc kết thúc.
- **color**: Màu của hình elip (BGR).
- **thickness**: 
  - Số dương: Độ dày của viền.
  - `cv.FILLED` hoặc `-1`: Tô đầy hình elip.
- **Ví dụ**:
  ```python
  cv.ellipse(blank, (250, 250), (150, 100), 0, 0, 360, (255, 255, 0), 2)  # Hình elip màu vàng
  ```

### e. Đa giác (Polygon)
```python
cv.polylines(IMAGE, [points], isClosed, color, thickness)
```
- **points**: Danh sách các điểm (mảng NumPy) tạo thành đa giác.
- **isClosed**: `True` nếu đa giác kín, `False` nếu không.
- **color**: Màu của đa giác (BGR).
- **thickness**: Độ dày của đường viền.
- **Ví dụ**:
  ```python
  points = np.array([[100, 100], [200, 50], [300, 100], [200, 200]], dtype=np.int32)
  cv.polylines(blank, [points], isClosed=True, color=(0, 255, 255), thickness=2)  # Đa giác màu vàng
  ```

### f. Viết chữ (Text)
```python
cv.putText(IMAGE, text, org, font, fontScale, color, thickness)
```
- **text**: Chuỗi văn bản cần vẽ.
- **org**: Tọa độ góc dưới bên trái của chữ (x, y).
- **font**: Kiểu chữ (ví dụ: `cv.FONT_HERSHEY_SIMPLEX`).
- **fontScale**: Kích thước chữ.
- **color**: Màu của chữ (BGR).
- **thickness**: Độ dày của chữ.
- **Ví dụ**:
  ```python
  cv.putText(blank, 'Hello OpenCV', (50, 400), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
  ```
