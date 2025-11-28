import cv2

# ...existing code...

def detect_digit(image_path):
    img = cv2.imread(image_path, 0)
    if img is None:
        print("Không tìm thấy hoặc không đọc được file ảnh!")
        return None
    img = cv2.medianBlur(img, 3)
    # Sử dụng THRESH_BINARY để số trắng giữ nguyên, nền đen vẫn là đen
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("Không tìm thấy contour nào!")
        return None

    # Loại bỏ contour nền (nếu có)
    img_area = img.shape[0] * img.shape[1]
    valid_contours = [c for c in contours if cv2.contourArea(c) < 0.9 * img_area]
    if not valid_contours:
        print("Không tìm thấy contour hợp lệ!")
        return None

    cnt = max(valid_contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)
    aspect_ratio = h / w
    area = cv2.contourArea(cnt)
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    solidity = float(area) / hull_area if hull_area != 0 else 0

    print(f"aspect_ratio: {aspect_ratio:.2f}, solidity: {solidity:.2f}")

    if aspect_ratio > 1.3 and solidity < 0.8:
        return 1
    else:
        return 0

def show_contours(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Không tìm thấy hoặc không đọc được file ảnh!")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_area = gray.shape[0] * gray.shape[1]
    valid_contours = [c for c in contours if cv2.contourArea(c) < 0.9 * img_area]
    img_contour = img.copy()
    cv2.drawContours(img_contour, valid_contours, -1, (0, 255, 0), 2)
    cv2.imshow('Contours', img_contour)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# # Ví dụ sử dụng:
# show_contours('C:/Users/63200744/Desktop/AI/FSB/IVP501/images/so0.jpg')
# show_contours('C:/Users/63200744/Desktop/AI/FSB/IVP501/images/so1.jpg')

print("Result so0:", detect_digit('C:/Users/63200744/Desktop/AI/FSB/IVP501/images/so0.jpg'))
print("Result so1:", detect_digit('C:/Users/63200744/Desktop/AI/FSB/IVP501/images/so1.jpg'))