# Bài 3: Mô hình Machine Learning đầu tiên của bạn

Bài học này hướng dẫn quy trình cơ bản để xây dựng mô hình machine learning bằng Python và thư viện scikit-learn, tập trung vào dự đoán giá nhà ở Melbourne.

## Các bước chính

1. **Chọn dữ liệu để xây dựng mô hình**
   - Xem các cột dữ liệu bằng `.columns`.
   - Loại bỏ các dòng có giá trị thiếu với `.dropna()`.

2. **Chọn biến mục tiêu**
   - Lấy cột cần dự đoán (ví dụ: `Price`) bằng dot notation.

3. **Chọn các đặc trưng (features)**
   - Chọn các cột liên quan để làm đặc trưng dự đoán.
   - Dùng danh sách tên cột để tạo tập features.

4. **Xây dựng mô hình**
   - Sử dụng `DecisionTreeRegressor` từ scikit-learn.
   - Định nghĩa mô hình và đặt `random_state` để kết quả nhất quán.
   - Fit mô hình với features và target.

5. **Dự đoán**
   - Dùng mô hình đã huấn luyện để dự đoán giá nhà cho dữ liệu mẫu.

## Quy trình ví dụ

- Load và làm sạch dữ liệu.
- Chọn biến mục tiêu và đặc trưng.
- Xây dựng và fit mô hình cây quyết định.
- Dự đoán trên dữ liệu mẫu.

Bài học này cung cấp nền tảng để xây dựng và đánh giá các mô hình machine learning đơn giản với Python.