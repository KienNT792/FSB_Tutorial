"""
Khái niệm: Các kỹ thuật chỉnh sửa histogram khác và kết quả khi áp dụng.
Ví dụ: Sử dụng CLAHE (Contrast Limited Adaptive Histogram Equalization).
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Đọc ảnh từ file
image = cv2.imread('C:/Users/63200744/Desktop/AI/FSB/IVP501/images/cameraman2.tif', cv2.IMREAD_GRAYSCALE)  # Đọc ảnh grayscale
if image is None:
    raise FileNotFoundError("Không tìm thấy ảnh tại đường dẫn đã cho.")

# Áp dụng CLAHE
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))  # Tạo đối tượng CLAHE
clahe_image = clahe.apply(image)  # Áp dụng CLAHE

# Hiển thị ảnh gốc và ảnh sau khi áp dụng CLAHE
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.title("Ảnh gốc")
plt.imshow(image, cmap='gray')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Ảnh sau khi áp dụng CLAHE")
plt.imshow(clahe_image, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()

# Hiển thị histogram trước và sau khi áp dụng CLAHE
hist_original = cv2.calcHist([image], [0], None, [256], [0, 256])
hist_clahe = cv2.calcHist([clahe_image], [0], None, [256], [0, 256])

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.title("Histogram gốc")
plt.plot(hist_original, color='k')
plt.xlabel("Mức độ sáng")
plt.ylabel("Tần suất")

plt.subplot(1, 2, 2)
plt.title("Histogram sau khi áp dụng CLAHE")
plt.plot(hist_clahe, color='k')
plt.xlabel("Mức độ sáng")
plt.ylabel("Tần suất")

plt.tight_layout()
plt.show()
