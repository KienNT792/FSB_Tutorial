# Chapter 10: Spatial Filtering - Xử lý ảnh trong miền không gian

## 1. Neighborhood Processing vs. Point Processing

### Point Processing (Xử lý điểm)
Là kỹ thuật mà giá trị pixel đầu ra tại vị trí $(x, y)$ **chỉ phụ thuộc duy nhất** vào giá trị pixel đầu vào tại chính vị trí đó. Nó không quan tâm đến các pixel xung quanh.
*   **Ví dụ:** Tăng độ sáng, chỉnh độ tương phản, phân ngưỡng (Thresholding), biến đổi âm bản (Negative).
*   **Công thức:** $g(x, y) = T[f(x, y)]$

### Neighborhood Processing (Xử lý lân cận)
Là kỹ thuật mà giá trị pixel đầu ra tại $(x, y)$ được tính toán dựa trên pixel tại $(x, y)$ **VÀ các pixel lân cận** (hàng xóm) của nó.
*   **Sự khác biệt:** Nó xem xét mối quan hệ không gian. Một pixel không đứng một mình mà chịu ảnh hưởng của môi trường xung quanh.
*   **Mục đích:** Dùng để làm mờ, làm sắc nét, khử nhiễu, dò biên.

> **Ví dụ trực quan:**
> *   *Point Processing:* Giống như việc chấm điểm thi cho một sinh viên chỉ dựa trên bài làm của họ.
> *   *Neighborhood Processing:* Giống như việc đánh giá hạnh kiểm của một sinh viên dựa trên cả những người bạn mà họ chơi cùng (gần mực thì đen, gần đèn thì rạng).

---

## 2. Convolution (Tích chập) là gì?

Convolution là phép toán cốt lõi để thực hiện Neighborhood Processing.

### Cơ chế hoạt động
Chúng ta sử dụng một ma trận nhỏ (thường là $3 \times 3$, $5 \times 5$) gọi là **Kernel** (hoặc Filter/Mask).
1.  Đặt Kernel lên trên ảnh, tâm Kernel trùng với pixel đang xét.
2.  Nhân từng giá trị trong Kernel với giá trị pixel tương ứng bên dưới nó.
3.  Cộng tổng tất cả các kết quả nhân lại.
4.  Gán tổng đó cho pixel ở vị trí tâm trong ảnh mới.
5.  Trượt (slide) Kernel sang pixel tiếp theo và lặp lại.

### Minh họa toán học
Giả sử Kernel $3 \times 3$ và vùng ảnh $3 \times 3$:

**Kernel:**
$$
\begin{bmatrix}
1 & 0 & 1 \\
0 & 1 & 0 \\
1 & 0 & 1
\end{bmatrix}
$$

**Vùng ảnh (Image Patch):**
$$
\begin{bmatrix}
10 & 20 & 30 \\
40 & 50 & 60 \\
70 & 80 & 90
\end{bmatrix}
$$

**Kết quả Convolution tại tâm:**
$(1\times10) + (0\times20) + (1\times30) + (0\times40) + (1\times50) + (0\times60) + (1\times70) + (0\times80) + (1\times90) = 250$

---

## 3. Low-pass Linear Filter (Bộ lọc thông thấp tuyến tính)

### Khái niệm
Trong xử lý tín hiệu, "tần số thấp" (low frequency) trong ảnh tương ứng với các vùng màu thay đổi chậm (vùng đồng màu, nền trời, da mặt mịn). "Tần số cao" là nơi thay đổi đột ngột (cạnh bàn, nhiễu).
*   **Low-pass filter:** Cho phép tần số thấp đi qua, chặn tần số cao.
*   **Tác dụng:** Làm mờ ảnh (Blurring), làm mịn (Smoothing), giảm nhiễu (Noise reduction).

### Cài đặt bằng 2D Convolution
Kernel của bộ lọc này thường có tất cả các giá trị là dương và tổng các phần tử bằng 1 (để giữ nguyên độ sáng trung bình của ảnh).

**Ví dụ: Bộ lọc trung bình (Average/Box Filter) $3 \times 3$**
$$
\frac{1}{9} \times
\begin{bmatrix}
1 & 1 & 1 \\
1 & 1 & 1 \\
1 & 1 & 1
\end{bmatrix}
$$

> **Kết quả thị giác:** Ảnh trở nên mờ đi, các chi tiết sắc cạnh bị nhòe, nhiễu hạt lấm tấm sẽ dịu bớt.

---

## 4. Median Filter (Bộ lọc trung vị)

### Khái niệm
Đây là bộ lọc **phi tuyến tính** (Non-linear). Nó không dùng phép nhân-cộng (convolution) như trên.
*   **Cách làm:** Tại mỗi vị trí cửa sổ trượt (ví dụ $3 \times 3$), ta lấy 9 giá trị pixel, **sắp xếp** chúng từ nhỏ đến lớn, và chọn giá trị nằm chính giữa (Median) để gán cho pixel đầu ra.

### Tác dụng đặc biệt
*   **Loại bỏ nhiễu muối tiêu (Salt-and-pepper noise):** Đây là loại nhiễu mà pixel đột ngột trắng xóa (255) hoặc đen sì (0).
*   **Tại sao dùng Median mà không dùng Low-pass (Average)?**
    *   Nếu dùng *Average*: Giá trị nhiễu (ví dụ 255) sẽ được cộng vào và chia trung bình, làm vùng đó bị nhòe đi nhưng vết bẩn vẫn còn mờ mờ.
    *   Nếu dùng *Median*: Giá trị 255 là ngoại lai (outlier), khi sắp xếp nó sẽ nằm ở cuối hàng và bị loại bỏ. Giá trị trung vị sẽ là một giá trị màu thực tế của vùng đó.

> **Kết quả thị giác:** Ảnh sạch nhiễu muối tiêu mà **không bị mờ biên** (edges preserved) nhiều như bộ lọc trung bình.

---

## 5. High-pass Linear Filter (Bộ lọc thông cao tuyến tính)

### Khái niệm
Ngược lại với Low-pass.
*   **High-pass filter:** Cho phép tần số cao (sự thay đổi đột ngột) đi qua, chặn tần số thấp (vùng đồng màu).
*   **Tác dụng:** Dò biên (Edge detection), làm sắc nét ảnh (Sharpening).

### Cài đặt bằng 2D Convolution
Kernel thường có giá trị dương ở tâm và giá trị âm ở xung quanh. Tổng các phần tử trong Kernel thường bằng 0 (để các vùng đồng màu sẽ triệt tiêu nhau thành màu đen).

**Ví dụ: Bộ lọc Laplacian (Dò biên)**
$$
\begin{bmatrix}
0 & -1 & 0 \\
-1 & 4 & -1 \\
0 & -1 & 0
\end{bmatrix}
$$
*(Lưu ý: $4 - 1 - 1 - 1 - 1 = 0$)*

> **Kết quả thị giác:**
> *   Vùng ảnh phẳng (bầu trời): Kết quả là màu đen (0).
> *   Vùng cạnh (biên dạng vật thể): Kết quả sẽ sáng lên.
> *   Ảnh kết quả trông như một bản vẽ phác thảo các đường nét.

---

## 3.1. Một số lưu ý thực tiễn khi xử lý lân cận
- Kích thước kernel càng lớn thì hiệu ứng làm mờ càng mạnh, nhưng cũng làm mất chi tiết ảnh.
- Khi áp dụng filter, các pixel ở biên ảnh (border) cần được xử lý đặc biệt (zero-padding, replicate, reflect, ...). OpenCV hỗ trợ nhiều chế độ border.
- Các filter tuyến tính (low-pass, high-pass) có thể kết hợp với nhau để tạo hiệu ứng phức tạp hơn.

---

## 3.2. Ví dụ code Python với OpenCV

### a) Low-pass filter (Làm mờ ảnh)
```python
import cv2
import numpy as np
img = cv2.imread('input.jpg', 0)  # Đọc ảnh xám
# Tạo kernel trung bình 3x3
kernel = np.ones((3,3), np.float32)/9
# cv2.filter2D: áp dụng convolution 2D, ddepth=-1 giữ nguyên kiểu dữ liệu ảnh
blur = cv2.filter2D(img, -1, kernel)
cv2.imwrite('blur.jpg', blur)
```

### b) Median filter (Khử nhiễu muối tiêu)
```python
import cv2
img = cv2.imread('input.jpg', 0)
# cv2.medianBlur: áp dụng bộ lọc trung vị, ksize là kích thước cửa sổ (lẻ)
median = cv2.medianBlur(img, 3)
cv2.imwrite('median.jpg', median)
```

### c) High-pass filter (Làm sắc nét, dò biên)
```python
import cv2
import numpy as np
img = cv2.imread('input.jpg', 0)
# Kernel Laplacian
kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
# cv2.filter2D: áp dụng convolution với kernel Laplacian
edges = cv2.filter2D(img, -1, kernel)
cv2.imwrite('edges.jpg', edges)
```

---

## 3.3. Một số ví dụ trực quan về hiệu ứng filter
- **Low-pass:** Ảnh chân dung sau khi làm mờ sẽ mất chi tiết tóc, da mịn hơn, nhiễu hạt giảm.
- **Median:** Ảnh bị nhiễu muối tiêu (nhiễu trắng đen lốm đốm) sau khi lọc sẽ sạch, biên vật thể vẫn rõ.
- **High-pass:** Ảnh phong cảnh sau khi áp dụng Laplacian sẽ nổi bật các đường biên, giống bản vẽ phác thảo.

---

## 3.4. Một số kernel phổ biến trong thực tế
- **Sharpening:**
  $$
  \begin{bmatrix}
  0 & -1 & 0 \\
  -1 & 5 & -1 \\
  0 & -1 & 0
  \end{bmatrix}
  $$
- **Gaussian Blur:**
  $$
  \frac{1}{16}
  \begin{bmatrix}
  1 & 2 & 1 \\
  2 & 4 & 2 \\
  1 & 2 & 1
  \end{bmatrix}
  $$
- **Sobel (Edge Detection):**
  $$
  G_x = \begin{bmatrix}-1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1\end{bmatrix},\quad
  G_y = \begin{bmatrix}-1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1\end{bmatrix}
  $$

---

## 3.5. Lưu ý khi lập trình với OpenCV
- Hàm `cv2.filter2D` cho phép áp dụng bất kỳ kernel nào, rất linh hoạt.
- Hàm `cv2.GaussianBlur`, `cv2.blur`, `cv2.medianBlur` là các hàm chuyên dụng cho từng loại filter.
- Khi xử lý ảnh màu, nên áp dụng filter trên từng kênh màu riêng biệt hoặc chuyển sang ảnh xám trước.
- Để so sánh hiệu ứng, nên hiển thị ảnh gốc và ảnh sau xử lý cạnh nhau.
