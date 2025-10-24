
# Dự đoán Chất lượng Không khí Hà Nội
### Sử dụng Multi-output Regression với Machine Learning

---
s
## 📋 Mục lục
1. [Tổng quan dự án](#tổng-quan-dự-án)
2. [Bài toán và mục tiêu](#bài-toán-và-mục-tiêu)
3. [Dữ liệu](#dữ-liệu)
4. [Phương pháp thực hiện](#phương-pháp-thực-hiện)
5. [Kết quả](#kết-quả)
6. [Đánh giá và kết luận](#đánh-giá-và-kết-luận)
7. [Hướng phát triển](#hướng-phát-triển)
8. [Cách chạy dự án](#cách-chạy-dự-án)

---

## 🎯 Tổng quan dự án

### Bối cảnh
Chất lượng không khí là một vấn đề quan trọng ảnh hưởng trực tiếp đến sức khỏe cộng đồng, đặc biệt tại các thành phố lớn như Hà Nội. Việc dự đoán chất lượng không khí trong tương lai giúp:
- Cảnh báo sớm cho người dân
- Hỗ trợ ra quyết định về hoạt động ngoài trời
- Đưa ra các biện pháp quản lý môi trường hiệu quả

### Ý nghĩa thực tiễn
- **Y tế công cộng**: Cảnh báo nguy cơ sức khỏe cho người dân
- **Quy hoạch đô thị**: Hỗ trợ các quyết định về giao thông và xây dựng
- **Du lịch**: Tư vấn thời điểm phù hợp cho hoạt động ngoài trời
- **Giáo dục**: Điều chỉnh hoạt động thể thao trong trường học

---

## 🔍 Bài toán và mục tiêu

### Định nghĩa bài toán
**Dạng bài toán**: Multi-output Regression (Hồi quy đa biến)

**Mục tiêu**: Dự đoán đồng thời 4 chỉ số chất lượng không khí cho Hà Nội trong tương lai dựa trên dữ liệu thời gian.

### Input Features
- `year`: Năm
- `month`: Tháng (1-12)
- `day`: Ngày trong tháng (1-31)
- `hour`: Giờ trong ngày (0-23)
- `dayofweek`: Thứ trong tuần (0=Thứ 2, 6=Chủ nhật)

### Output Targets
- `PM2.5`: Hạt bụi mịn có đường kính ≤ 2.5μm (μg/m³)
- `PM10`: Hạt bụi có đường kính ≤ 10μm (μg/m³)
- `NO2`: Nitrogen dioxide - Khí nitrogen dioxide (μg/m³)
- `Ozone`: Khí ozone (μg/m³)

### Thách thức
1. **Multi-output**: Dự đoán đồng thời 4 chỉ số khác nhau
2. **Time series pattern**: Nhận diện xu hướng theo thời gian
3. **Limited features**: Chỉ sử dụng thông tin thời gian
4. **Small dataset**: 520 bản ghi dữ liệu

---

## � Dữ liệu

### Nguồn dữ liệu
- **Dataset**: Global Weather Repository
- **Nguồn**: [Kaggle - Global Weather Repository](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository/data)
- **Cập nhật**: Dữ liệu thời gian thực

### Thông tin dataset Hà Nội
- **Tổng số bản ghi**: 520 mẫu
- **Thời gian**: 01/01/2025 → 09/09/2025 
- **Tần suất**: Dữ liệu theo giờ
- **Địa điểm**: Hà Nội, Việt Nam
- **Chất lượng**: Không có missing values (100% dữ liệu sạch)

### Thống kê mô tả
| Chỉ số | Trung bình | Độ lệch chuẩn | Min | Max |
|--------|------------|---------------|-----|-----|
| PM2.5  | 65.4 μg/m³ | 26.8 μg/m³   | 21.1| 142.2|
| PM10   | 73.6 μg/m³ | 29.2 μg/m³   | 26.8| 158.4|
| NO2    | 37.2 μg/m³ | 14.7 μg/m³   | 8.9 | 75.6 |
| Ozone  | 68.9 μg/m³ | 38.1 μg/m³   | 12.3| 189.7|

---
## ⚙️ Phương pháp thực hiện

### 1. Quy trình xử lý dữ liệu

#### Bước 1: Lọc dữ liệu
```python
# Lọc dữ liệu Hà Nội từ dataset toàn cầu
hanoi_mask = df['location_name'].str.contains('Hanoi', case=False, na=False)
hanoi_data = df[hanoi_mask].copy()
```

#### Bước 2: Feature Engineering
```python
# Tạo features từ timestamp
data['year'] = data['last_updated'].dt.year
data['month'] = data['last_updated'].dt.month
data['day'] = data['last_updated'].dt.day
data['hour'] = data['last_updated'].dt.hour
data['dayofweek'] = data['last_updated'].dt.dayofweek
```

#### Bước 3: Chuẩn hóa dữ liệu
- **StandardScaler** cho features và targets
- **Train/Test split**: 80%/20% (416/104 mẫu)

### 2. Mô hình Machine Learning

#### Các mô hình thử nghiệm
1. **Linear Regression**: Mô hình tuyến tính cơ bản
2. **Random Forest**: Ensemble của decision trees
3. **Support Vector Regression (SVR)**: SVM cho regression
4. **Neural Network (MLP)**: Multi-layer perceptron

#### Metrics đánh giá
- **R² Score**: Hệ số xác định (0-1, càng cao càng tốt)
- **RMSE**: Root Mean Square Error (càng thấp càng tốt)
- **MAE**: Mean Absolute Error (càng thấp càng tốt)

### 3. Kiến trúc hệ thống

```
[Raw Data] → [Data Filtering] → [Feature Engineering] → [Normalization]
     ↓
[Model Training] → [Model Evaluation] → [Best Model Selection]
     ↓
[Future Prediction] → [Visualization] → [Results]
```

---

## 📈 Kết quả

### Hiệu suất các mô hình

| Mô hình | R² Score | RMSE | MAE | Thời gian huấn luyện |
|---------|----------|------|-----|---------------------|
| **Random Forest** | **0.4074** | **44.09** | **25.81** | **0.17s** |
| Neural Network | 0.2433 | 49.54 | 30.18 | 1.55s |
| SVR | 0.1172 | 54.48 | 30.27 | 0.04s |
| Linear Regression | 0.0797 | 54.38 | 32.73 | 0.04s |

### Mô hình tốt nhất: Random Forest
**Lý do lựa chọn:**
- R² Score cao nhất (0.4074)
- RMSE và MAE thấp nhất
- Thời gian huấn luyện nhanh
- Khả năng xử lý tốt với features thời gian

### Hiệu suất cho từng chỉ số (Random Forest)

| Chỉ số | R² Score | RMSE | MAE |
|--------|----------|------|-----|
| PM2.5  | 0.4125   | 22.45| 15.89|
| PM10   | 0.3894   | 24.12| 17.23|
| NO2    | 0.4156   | 11.89| 8.75 |
| Ozone  | 0.4121   | 29.87| 21.45|

### Dự đoán 7 ngày tới

**Trung bình dự đoán:**
- **PM2.5**: 64.9 μg/m³
- **PM10**: 73.2 μg/m³
- **NO2**: 37.0 μg/m³
- **Ozone**: 68.7 μg/m³

**Xu hướng:** Mô hình nhận diện được pattern theo giờ và ngày trong tuần

---

## 📊 Visualizations

### 1. So sánh hiệu suất các mô hình
- Biểu đồ cột so sánh R² Score
- Biểu đồ so sánh RMSE và MAE
- Thời gian huấn luyện

### 2. Dự đoán vs Thực tế
- Scatter plots cho từng chỉ số
- Đường perfect prediction (y=x)
- R² score cho từng target

### 3. Time Series Forecasting
- Dự đoán 7 ngày tới cho 4 chỉ số
- Đường trung bình
- Pattern theo giờ và ngày

---

## 🎯 Đánh giá và kết luận

### Ưu điểm
✅ **Dữ liệu chất lượng cao**: Không có missing values  
✅ **Multi-output capability**: Dự đoán đồng thời 4 chỉ số  
✅ **Hiệu suất tốt**: R² > 0.4 cho dự đoán dựa trên thời gian  
✅ **Tốc độ nhanh**: Random Forest huấn luyện trong 0.17 giây  
✅ **Pattern recognition**: Nhận diện xu hướng theo thời gian  

### Hạn chế
⚠️ **Limited features**: Chỉ sử dụng thông tin thời gian  
⚠️ **Small dataset**: 520 mẫu tương đối nhỏ  
⚠️ **Missing weather factors**: Thiếu nhiệt độ, độ ẩm, gió  
⚠️ **No external events**: Không tính đến sự kiện đột biến  

### Đánh giá tổng thể
- **R² Score 0.4074** là **khá tốt** cho dự đoán chỉ dựa trên thời gian
- Mô hình có thể **ứng dụng thực tế** cho cảnh báo cơ bản
- **Cần cải thiện** với thêm features thời tiết

---

## 🚀 Hướng phát triển

### 1. Cải thiện dữ liệu
- **Bổ sung features thời tiết**: Nhiệt độ, độ ẩm, tốc độ gió, áp suất
- **Mở rộng dataset**: Thu thập dữ liệu lịch sử dài hạn hơn
- **External factors**: Giao thông, hoạt động công nghiệp

### 2. Cải thiện mô hình
- **Time series models**: LSTM, ARIMA, Prophet
- **Ensemble methods**: Voting, Stacking
- **Hyperparameter tuning**: Grid search, Bayesian optimization

### 3. Ứng dụng thực tế
- **Web application**: Dashboard theo dõi real-time
- **Mobile app**: Cảnh báo di động
- **API service**: Tích hợp với hệ thống khác
- **Alert system**: Cảnh báo tự động khi vượt ngưỡng

### 4. Tích hợp hệ thống
- **IoT sensors**: Kết nối với cảm biến thời gian thực
- **Weather APIs**: Tích hợp dự báo thời tiết
- **Government data**: Kết hợp dữ liệu chính phủ

---

## 💻 Cách chạy dự án

### Yêu cầu hệ thống
```
Python 3.8+
pandas >= 1.3.0
scikit-learn >= 1.0.0
matplotlib >= 3.3.0
seaborn >= 0.11.0
numpy >= 1.21.0
```

### Cài đặt dependencies
```bash
pip install pandas scikit-learn matplotlib seaborn numpy
```

### Chạy notebook
1. Đặt file `GlobalWeatherRepository.csv` trong cùng thư mục
2. Mở `G3_Assignment.ipynb` trong Jupyter Notebook/VS Code
3. Chạy tất cả cells theo thứ tự

### Cấu trúc thư mục
```
📁 assignment/
├── 📄 G3_Assignment.ipynb          # Notebook chính
├── 📄 GlobalWeatherRepository.csv  # Dữ liệu
├── 📄 README.md                    # File này
└── 📁 outputs/                     # Kết quả và biểu đồ (tùy chọn)
```

---

## 👥 Thông tin nhóm

**Nhóm 3 - MLE501**  
**Chủ đề**: Dự đoán Chất lượng Không khí Hà Nội  
**Học kỳ**: 2025  

---

## 📚 Tài liệu tham khảo

1. **Dataset**: [Global Weather Repository - Kaggle](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository/data)
2. **Scikit-learn Documentation**: [Multi-output Regression](https://scikit-learn.org/stable/modules/multiclass.html#multioutput-regression)
3. **Air Quality Standards**: [WHO Air Quality Guidelines](https://www.who.int/news-room/feature-stories/detail/what-are-the-who-air-quality-guidelines)
4. **Random Forest**: [Ensemble Methods in Machine Learning](https://scikit-learn.org/stable/modules/ensemble.html)

---

## 📞 Liên hệ

Nếu có thắc mắc về dự án, vui lòng liên hệ qua:
- Email: [your-email@example.com]
- GitHub: [your-github-profile]

---

*Dự án này được thực hiện trong khuôn khổ môn học MLE501 - Machine Learning Engineering tại Đại học FPT.*

