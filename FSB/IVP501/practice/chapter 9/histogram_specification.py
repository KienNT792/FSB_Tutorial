"""
Khái niệm: Histogram specification và tác động của nó lên ảnh.
Ví dụ: Chuyển đổi histogram của ảnh grayscale theo histogram mục tiêu.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def match_histograms(source, template):
    """
    Hàm thực hiện histogram specification (match histogram của ảnh source với ảnh template).
    """
    source_hist, bins = np.histogram(source.flatten(), 256, [0, 256])
    template_hist, _ = np.histogram(template.flatten(), 256, [0, 256])

    # Tính CDF
    source_cdf = np.cumsum(source_hist) / np.sum(source_hist)
    template_cdf = np.cumsum(template_hist) / np.sum(template_hist)

    # Tạo mapping từ source sang template
    mapping = np.interp(source_cdf, template_cdf, np.arange(256))

    # Áp dụng mapping
    matched = np.interp(source.flatten(), bins[:-1], mapping).reshape(source.shape)
    return matched.astype(np.uint8)

# Đọc ảnh nguồn và ảnh mục tiêu
source_image = cv2.imread('source_image.jpg', cv2.IMREAD_GRAYSCALE)  # Ảnh nguồn
template_image = cv2.imread('template_image.jpg', cv2.IMREAD_GRAYSCALE)  # Ảnh mục tiêu
if source_image is None or template_image is None:
    raise FileNotFoundError("Không tìm thấy ảnh nguồn hoặc ảnh mục tiêu.")

# Thực hiện histogram specification
matched_image = match_histograms(source_image, template_image)

# Hiển thị ảnh
plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
plt.title("Ảnh nguồn")
plt.imshow(source_image, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title("Ảnh mục tiêu")
plt.imshow(template_image, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title("Ảnh sau khi match histogram")
plt.imshow(matched_image, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()
