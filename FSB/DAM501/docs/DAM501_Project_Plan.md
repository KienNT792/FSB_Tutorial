# Kế hoạch Dự án Khai phá Dữ liệu: Dự đoán PM2.5 tại Hà Nội

## 1. Tổng quan dự án

- Chủ đề: Dự đoán chỉ số PM2.5 tại Hà Nội.
- Mục tiêu: Phát triển mô hình học máy để dự đoán nồng độ PM2.5 dựa trên dữ liệu lịch sử về thời tiết và chất lượng không khí.
- Phương pháp luận: CRISP-DM (Cross Industry Standard Process for Data Mining).

## 2. Nguồn dữ liệu

- Dữ liệu thời tiết: `hanoi_weather_history.csv`
  - Thuộc tính: Nhiệt độ (`temp`), Độ ẩm (`rh`), Tốc độ gió (`wind_spd`), Hướng gió (`wind_dir`), Áp suất (`pres`), Tầm nhìn (`vis`), Chỉ số UV (`uv`), v.v.
  - Tần suất: Theo giờ.
- Dữ liệu chất lượng không khí: `hanoi_air_quality_history.csv`
  - Thuộc tính: PM2.5, PM10, AQI, CO, NO2, O3, SO2.
  - Tần suất: Theo giờ.

## 3. Kế hoạch triển khai

### Giai đoạn 1: Hiểu dữ liệu & Phân tích Khám phá (EDA)

- Mục tiêu: Hiểu phân bố dữ liệu, tương quan và chất lượng dữ liệu.
- Công việc:
  - Nạp và kiểm tra cấu trúc dữ liệu.
  - Kiểm tra giá trị khuyết (missing values) và điểm ngoại lai (outliers).
  - Trực quan hóa:
    - Biểu đồ chuỗi thời gian cho PM2.5 và các biến thời tiết.
    - Bản đồ nhiệt tương quan (Pearson) để tìm yếu tố ảnh hưởng chính đến PM2.5 (ví dụ: tương quan giữa `pm25` với `wind_spd`, `temp`, `rh`).
    - Biểu đồ phân bố (Histogram/Boxplot).

### Giai đoạn 2: Tiền xử lý dữ liệu

- Mục tiêu: Chuẩn bị bộ dữ liệu sạch cho việc xây dựng mô hình.
- Công việc:
  - Làm sạch dữ liệu: Xử lý giá trị khuyết (nội suy theo thời gian hoặc trung bình/trung vị).
  - Gộp dữ liệu: Merge dữ liệu Thời tiết và Chất lượng không khí theo cột `datetime`.
  - Chọn thuộc tính: Loại bỏ cột không liên quan (vd: `uv` nếu hầu hết là 0, hoặc các thuộc tính dư thừa có tương quan cao).
  - Kỹ thuật đặc trưng:
    - Thuộc tính thời gian: Trích xuất Giờ, Thứ trong tuần, Tháng, Mùa.
    - Thuộc tính trễ: Tạo biến trễ (vd: `pm25_lag_1h`, `temp_lag_1h`) để bắt tính phụ thuộc theo thời gian.
    - Thống kê trượt: Trung bình/độ lệch chuẩn trượt theo cửa sổ (vd: 24 giờ).

### Giai đoạn 3: Phát triển mô hình

- Mục tiêu: Huấn luyện các mô hình dự đoán.
- Biến mục tiêu: `pm25` (bài toán hồi quy).
- Mô hình ứng viên:
  1. Hồi quy tuyến tính (Linear Regression): Mô hình baseline.
  2. Rừng ngẫu nhiên (Random Forest Regressor): Xử lý tốt quan hệ phi tuyến.
  3. XGBoost/LightGBM: Gradient boosting cho hiệu năng cao.
  4. LSTM (Long Short-Term Memory): Học sâu cho chuỗi thời gian (tùy chọn nếu cần cách tiếp cận nâng cao).
- Cách chia dữ liệu:
  - Train-Test Split (ví dụ: 80% Train, 20% Test).
  - Quan trọng: Sử dụng chia theo thời gian (không xáo trộn ngẫu nhiên) để tránh rò rỉ dữ liệu.

### Giai đoạn 4: Đánh giá

- Mục tiêu: Đánh giá hiệu năng mô hình.
- Thước đo:
  - RMSE (Root Mean Squared Error): Nhấn mạnh lỗi lớn.
  - MAE (Mean Absolute Error): Độ lớn lỗi trung bình.
  - R² Score: Tỷ lệ phương sai được giải thích bởi mô hình.
- Thẩm định: So sánh hiệu năng mô hình với baseline.

## 4. Công cụ & Thư viện

- Ngôn ngữ: Python
- Thư viện: Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, XGBoost.

## 5. Lộ trình thời gian (ước tính)

1. Nạp dữ liệu & EDA: 20%
2. Tiền xử lý & Kỹ thuật đặc trưng: 30%
3. Huấn luyện mô hình: 30%
4. Đánh giá & Báo cáo: 20%

> Lưu ý: Kế hoạch này giả định mục tiêu hồi quy tiêu chuẩn. Nếu tài liệu “Final project description.pdf” có yêu cầu cụ thể (ví dụ: phân loại mức AQI thay vì hồi quy, hoặc yêu cầu về chân trời dự báo), kế hoạch sẽ cần điều chỉnh tương ứng.