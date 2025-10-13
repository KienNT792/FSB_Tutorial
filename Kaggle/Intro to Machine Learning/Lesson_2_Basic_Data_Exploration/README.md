# Bài 2: Khám phá dữ liệu cơ bản với Pandas

Bài học này giới thiệu cách sử dụng thư viện Pandas để khám phá và hiểu dữ liệu, là bước đầu tiên trong mọi dự án Machine Learning.

## Các khái niệm chính

1. **Pandas và DataFrame**
   - Pandas là thư viện Python mạnh mẽ dùng để phân tích dữ liệu.
   - Cấu trúc dữ liệu quan trọng nhất là DataFrame, lưu trữ dữ liệu dạng bảng giống như Excel hoặc SQL.

2. **Nạp dữ liệu**
   - Dùng `pd.read_csv()` để đọc dữ liệu từ file CSV vào DataFrame.

3. **Xem dữ liệu**
   - Dùng `.head()` để xem một vài dòng đầu tiên của dataset.

4. **Mô tả dữ liệu**
   - Dùng `.describe()` để lấy các thống kê tổng quan cho từng cột, gồm:
     - `count`: số lượng giá trị không thiếu
     - `mean`: giá trị trung bình
     - `std`: độ lệch chuẩn
     - `min`, `25%`, `50%`, `75%`, `max`: các giá trị phân vị và cực trị

5. **Hiểu ý nghĩa các thống kê**
   - Dùng kết quả từ `.describe()` để hiểu phân bố và mức độ biến động của dữ liệu.
   - Phát hiện giá trị thiếu và ngoại lệ.

## Quy trình ví dụ

- Import Pandas và nạp dữ liệu.
- Xem các dòng mẫu và thống kê tổng quan.
- Sử dụng các thông tin này để định hướng các bước xử lý dữ liệu tiếp theo.

Bài học này giúp bạn làm quen với việc khám phá và chuẩn bị dữ liệu trước khi xây dựng mô hình machine learning.