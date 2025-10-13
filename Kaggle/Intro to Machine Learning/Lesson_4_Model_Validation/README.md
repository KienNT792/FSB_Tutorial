# Bài 4: Đánh giá Mô hình (Model Validation)

Bài học này hướng dẫn cách đánh giá chất lượng mô hình machine learning bằng kỹ thuật “model validation”.

## Các khái niệm chính

1. **Model Validation là gì?**
   - Đánh giá xem mô hình dự đoán có chính xác không, thường dùng độ chính xác dự đoán (predictive accuracy).

2. **Sai lầm thường gặp**
   - Đánh giá mô hình trên chính dữ liệu huấn luyện sẽ khiến mô hình chỉ “ghi nhớ” dữ liệu, không tổng quát hoá cho dữ liệu mới.

3. **Metric đánh giá: MAE (Mean Absolute Error)**
   - MAE đo sai số tuyệt đối trung bình giữa giá trị thực tế và giá trị dự đoán.
   - MAE càng nhỏ, mô hình càng chính xác.

4. **Vấn đề với “In-Sample Scores”**
   - Đánh giá trên dữ liệu huấn luyện dễ bị ảo tưởng về chất lượng mô hình.

5. **Tại sao cần Validation Data**
   - Chia dữ liệu thành training set và validation set để kiểm tra mô hình trên dữ liệu chưa từng thấy.
   - Đánh giá trên validation set phản ánh thực tế hơn về khả năng dự đoán của mô hình.

## Quy trình ví dụ

- Chia dữ liệu thành training và validation set bằng `train_test_split`.
- Huấn luyện mô hình trên training set.
- Dự đoán và tính MAE trên validation set để đánh giá mô hình.

Bài học này giúp bạn biết cách kiểm tra và so sánh chất lượng các mô hình machine learning một cách khách quan.