# 📉 Hiện tượng Underfitting và Overfitting trong Machine Learning

## 🔍 Khái niệm

- **Underfitting**: Xảy ra khi mô hình quá đơn giản, không học được các mối quan hệ quan trọng trong dữ liệu, dẫn đến hiệu suất kém cả trên dữ liệu huấn luyện và kiểm định.

- **Overfitting**: Xảy ra khi mô hình quá phức tạp, học quá chi tiết các đặc điểm của dữ liệu huấn luyện, bao gồm cả nhiễu, dẫn đến hiệu suất rất tốt trên dữ liệu huấn luyện nhưng kém trên dữ liệu kiểm định.

---

## 📖 Story minh họa

Bài học dùng ví dụ về **giá nhà**:  

- Một mô hình quá **đơn giản** (underfitting) có thể chỉ dự đoán **giá trung bình cho tất cả các nhà**, bỏ qua các yếu tố như số phòng, diện tích, hay năm xây dựng.  
  - Kết quả: Sai số lớn trên cả dữ liệu huấn luyện và kiểm định.  

- Một mô hình quá **phức tạp** (overfitting) lại học **chi tiết từng đặc điểm nhỏ** trong dữ liệu huấn luyện, ví dụ: ngôi nhà có cửa màu xanh lá → giá cao, hoặc sàn gỗ → giá thấp, ngay cả khi điều đó **không phản ánh thực tế**.  
  - Kết quả: Sai số thấp trên dữ liệu huấn luyện nhưng **cao trên dữ liệu kiểm định**.

- Mục tiêu: Tìm ra mô hình **đúng vừa đủ** để học được các mẫu quan trọng, nhưng **không học cả nhiễu**.

---

## ⚠️ Nguyên nhân và Hậu quả

- **Underfitting**: Mô hình không đủ phức tạp để nắm bắt các mẫu trong dữ liệu, dẫn đến hiệu suất kém.

- **Overfitting**: Mô hình học quá chi tiết, bao gồm cả nhiễu trong dữ liệu huấn luyện, dẫn đến hiệu suất kém khi gặp dữ liệu mới.

---

## 🛠️ Giải pháp

- **Giảm độ phức tạp của mô hình**: Sử dụng các mô hình đơn giản hơn để tránh overfitting.

- **Thu thập thêm dữ liệu**: Dữ liệu phong phú giúp mô hình học được các mẫu chung hơn.

- **Sử dụng kỹ thuật Regularization**: Giới hạn độ phức tạp của mô hình để tránh overfitting.

- **Sử dụng Cross-validation**: Đánh giá mô hình trên nhiều tập dữ liệu khác nhau để kiểm tra khả năng tổng quát.

---

## 📈 Tầm quan trọng

Hiểu và kiểm soát underfitting và overfitting là chìa khóa để xây dựng mô hình machine learning hiệu quả, có khả năng tổng quát tốt và hoạt động ổn định trên dữ liệu mới.
