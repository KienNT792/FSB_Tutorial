"""
Khái niệm: Histogram của ảnh là một biểu đồ biểu diễn phân bố tần suất của các mức độ sáng (intensity levels) trong ảnh.
Ví dụ: Đọc ảnh và vẽ histogram của ảnh grayscale và ảnh màu RGB.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Đọc ảnh từ file
image = cv2.imread('C:/Users/63200744/Desktop/AI/FSB/IVP501/images/cameraman2.tif')  # Đọc ảnh từ đường dẫn
if image is None:
    raise FileNotFoundError("Không tìm thấy ảnh tại đường dẫn đã cho.")

# Chuyển ảnh sang grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Chuyển ảnh sang grayscale

# Tính histogram cho ảnh grayscale
hist_gray = cv2.calcHist([gray_image], [0], None, [256], [0, 256])  # Tính histogram

# Tính histogram cho ảnh màu RGB
colors = ('b', 'g', 'r')
hist_rgb = {}
for i, color in enumerate(colors):
    hist_rgb[color] = cv2.calcHist([image], [i], None, [256], [0, 256])  # Tính histogram cho từng kênh màu

# Vẽ histogram
plt.figure(figsize=(12, 6))

# Histogram ảnh grayscale
plt.subplot(1, 2, 1)
plt.title("Histogram của ảnh Grayscale")
plt.plot(hist_gray, color='k')
plt.xlabel("Mức độ sáng")
plt.ylabel("Tần suất")

# Histogram ảnh RGB
plt.subplot(1, 2, 2)
plt.title("Histogram của ảnh RGB")
for color, hist in hist_rgb.items():
    plt.plot(hist, color=color)
plt.xlabel("Mức độ sáng")
plt.ylabel("Tần suất")

plt.tight_layout()
plt.show()
