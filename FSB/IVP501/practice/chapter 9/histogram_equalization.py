"""
Khái niệm: Histogram equalization và tác động của nó lên ảnh.
Ví dụ: Cân bằng histogram của ảnh grayscale.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Đọc ảnh từ file
image = cv2.imread('C:/Users/63200744/Desktop/AI/FSB/IVP501/images/cameraman2.tif', cv2.IMREAD_GRAYSCALE)  # Đọc ảnh grayscale
if image is None:
    raise FileNotFoundError("Không tìm thấy ảnh tại đường dẫn đã cho.")

# Cân bằng histogram
equalized_image = cv2.equalizeHist(image)  # Cân bằng histogram

# Hiển thị ảnh gốc và ảnh sau khi cân bằng
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.title("Ảnh gốc")
plt.imshow(image, cmap='gray')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Ảnh sau khi cân bằng histogram")
plt.imshow(equalized_image, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()

# Hiển thị histogram trước và sau khi cân bằng
hist_original = cv2.calcHist([image], [0], None, [256], [0, 256])
hist_equalized = cv2.calcHist([equalized_image], [0], None, [256], [0, 256])

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.title("Histogram gốc")
plt.plot(hist_original, color='k')
plt.xlabel("Mức độ sáng")
plt.ylabel("Tần suất")

plt.subplot(1, 2, 2)
plt.title("Histogram sau khi cân bằng")
plt.plot(hist_equalized, color='k')
plt.xlabel("Mức độ sáng")
plt.ylabel("Tần suất")

plt.tight_layout()
plt.show()
