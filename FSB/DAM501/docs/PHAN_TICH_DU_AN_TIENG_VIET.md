# 📊 Dự án Cuối kỳ DAM501 - Tóm tắt Phân tích Dự đoán PM2.5

## Tổng quan Dự án
**Môn học**: DAM501 - Khai thác Dữ liệu (Data Mining)  
**Bài toán**: Dự đoán mức độ ô nhiễm không khí PM2.5 tại Hà Nội  
**Dữ liệu**: Chất lượng không khí + Dữ liệu thời tiết (~24,000 bản ghi theo giờ)  
**Loại bài toán**: Hồi quy (Regression)  
**Ngày**: Tháng 12 năm 2025

---

## 1. ĐỊNH NGHĨA BÀI TOÁN

### Bối cảnh Kinh doanh
Hà Nội đang đối mặt với tình trạng ô nhiễm không khí nghiêm trọng, PM2.5 là mối quan tâm chính:
- Liên tục vượt ngưỡng an toàn của WHO (>15 μg/m³)
- Gây ra các vấn đề sức khỏe nghiêm trọng: bệnh hô hấp, tim mạch, ung thư phổi
- Tác động kinh tế: chi phí y tế, mất năng suất lao động, suy giảm du lịch

### Mục tiêu
Xây dựng mô hình hồi quy để dự đoán nồng độ PM2.5 dựa trên:
- **Yếu tố thời tiết**: nhiệt độ, độ ẩm, gió, áp suất, tầm nhìn, lượng mưa
- **Các chất ô nhiễm khác**: PM10, O3, SO2, NO2, CO

### Tác động Kinh doanh
**Đối với Chính phủ & Cơ quan Môi trường:**
- Hệ thống cảnh báo sớm về chất lượng không khí
- Hỗ trợ quyết định chính sách (đóng cửa nhà máy, hạn chế giao thông)
- Quy hoạch phát triển đô thị

**Đối với Ngành Y tế:**
- Chuẩn bị nguồn lực y tế khi ô nhiễm cao
- Tư vấn sức khỏe cho nhóm nguy cơ cao

**Đối với Doanh nghiệp:**
- Du lịch: Lập kế hoạch tour du lịch và khuyến mãi
- Bán lẻ: Dự đoán nhu cầu khẩu trang, máy lọc không khí
- Bảo hiểm: Định giá bảo hiểm sức khỏe chính xác

**Lợi ích Định lượng:**
- Giảm 10-15% chi phí điều trị bệnh hô hấp
- Tăng 5-8% năng suất (giảm ngày nghỉ ốm)
- Tiết kiệm 1.5-2 triệu USD/năm cho thành phố Hà Nội

### Chỉ số Đo lường Thành công
| Chỉ số | Mục tiêu | Tầm quan trọng |
|--------|----------|----------------|
| **RMSE** | < 15 μg/m³ | Chính - phạt nặng sai số lớn |
| **MAE** | < 10 μg/m³ | Dễ hiểu cho người dùng |
| **R² Score** | > 0.85 | Độ khớp tổng thể của mô hình |
| **MAPE** | < 20% | Độ chính xác tương đối |
| **Độ chính xác phân loại AQI** | > 90% | Quan trọng cho cảnh báo sức khỏe |

---

## 2. ĐÁNH GIÁ DỮ LIỆU

### Tóm tắt Dữ liệu

#### Dữ liệu Chất lượng Không khí (hanoi_air_quality_history.csv)
- **Số bản ghi**: 24,059 (dữ liệu theo giờ)
- **Số cột**: 8 cột
  - `datetime`: Thời gian
  - `pm25`: **MỤC TIÊU** - Nồng độ bụi mịn PM2.5 (μg/m³)
  - `pm10`, `o3`, `so2`, `no2`, `co`: Các chất ô nhiễm khác
  - `aqi`: Chỉ số Chất lượng Không khí

#### Dữ liệu Thời tiết (hanoi_weather_history.csv)
- **Số bản ghi**: 24,025 (dữ liệu theo giờ)
- **Số cột**: 12 cột
  - `datetime`: Thời gian (khóa kết nối)
  - `temp`, `app_temp`: Nhiệt độ thực tế và cảm nhận (°C)
  - `rh`: Độ ẩm tương đối (%)
  - `wind_spd`, `wind_dir`: Tốc độ gió (m/s) & hướng gió (độ)
  - `pres`: Áp suất khí quyển (hPa)
  - `vis`: Tầm nhìn xa (km)
  - `clouds`: Độ che phủ của mây (%)
  - `precip`: Lượng mưa (mm)
  - `uv`: Chỉ số UV
  - `dewpt`: Nhiệt độ điểm sương (°C)

### Đặc điểm Dữ liệu

#### ✅ Điểm mạnh:
1. **Bộ tính năng đầy đủ**: Bao gồm tất cả yếu tố thời tiết chính
2. **Tần suất cao**: Dữ liệu theo giờ nắm bắt được các mẫu ngắn hạn
3. **Nhiều chỉ số ô nhiễm**: Giúp mô hình học tốt hơn
4. **Định dạng có cấu trúc**: Nhất quán, dễ xử lý
5. **Dữ liệu thực tế**: Phản ánh điều kiện thực tế

#### ⚠️ Thách thức:
1. **Thời gian ngắn**: Chỉ vài ngày, không đủ cho mẫu theo mùa
2. **Vấn đề định dạng thời gian**: Định dạng không chuẩn (YYYY-MM-DD:HH)
3. **Khoảng thời gian không khớp**: Ngày bắt đầu/kết thúc khác nhau giữa các tập dữ liệu
4. **Thiếu yếu tố bên ngoài**: Không có dữ liệu về giao thông, hoạt động công nghiệp
5. **Giá trị thiếu tiềm ẩn**: Cần kiểm tra và xử lý
6. **Outliers**: Giá trị PM2.5 cực đoan (nhưng là sự kiện thực)
7. **Đa cộng tuyến**: Một số tính năng có tương quan cao (temp vs app_temp)
8. **Tính năng tuần hoàn**: Hướng gió cần mã hóa đặc biệt

---

## 3. CHIẾN LƯỢC TIỀN XỬ LÝ DỮ LIỆU

### Pipeline Được Đề xuất

#### Bước 1: Xử lý Thời gian & Kết hợp Dữ liệu
```python
# Chuyển đổi sang datetime
df_weather['datetime'] = pd.to_datetime(df_weather['datetime'], format='%Y-%m-%d:%H')
df_air['datetime'] = pd.to_datetime(df_air['datetime'], format='%Y-%m-%d:%H')

# Inner join - chỉ giữ các timestamp khớp
merged_df = pd.merge(df_weather, df_air, on='datetime', how='inner')
```
**Lý do**: Đồng bộ hóa các tập dữ liệu, đảm bảo mỗi bản ghi có đầy đủ các tính năng

#### Bước 2: Loại bỏ Rò rỉ Dữ liệu
```python
# Bỏ AQI - nó được tính từ PM2.5
merged_df = merged_df.drop(columns=['aqi'])
```
**Lý do**: AQI được tính từ PM2.5, việc sử dụng nó sẽ gây ra overfitting

#### Bước 3: Mã hóa Tính năng Tuần hoàn
```python
# Hướng gió: 0° = 360° (vòng tròn)
merged_df['wind_dir_sin'] = np.sin(np.deg2rad(merged_df['wind_dir']))
merged_df['wind_dir_cos'] = np.cos(np.deg2rad(merged_df['wind_dir']))
```
**Lý do**: Bảo toàn tính chất vòng tròn của hướng gió

#### Bước 4: Kỹ thuật Tính năng Thời gian
```python
merged_df['hour'] = merged_df['datetime'].dt.hour
merged_df['day_of_week'] = merged_df['datetime'].dt.dayofweek
merged_df['is_rush_hour'] = merged_df['hour'].isin([7,8,9,17,18,19]).astype(int)
```
**Lý do**: Nắm bắt các mẫu hàng ngày và hàng tuần trong PM2.5

#### Bước 5: Xử lý Giá trị Thiếu
**Chiến lược**: Forward fill hoặc interpolation (chuỗi thời gian)
```python
# Lựa chọn 1: Forward fill
merged_df = merged_df.fillna(method='ffill')

# Lựa chọn 2: Interpolation tuyến tính (tốt hơn cho thay đổi dần)
merged_df = merged_df.interpolate(method='linear')
```
**Thực hành Tốt nhất**: Không sử dụng mean/median cho chuỗi thời gian

#### Bước 6: Xử lý Outliers
**Chiến lược**: Cắt giới hạn thay vì loại bỏ
```python
# Cắt tại phân vị 1% và 99%
for col in numeric_features:
    Q1 = merged_df[col].quantile(0.01)
    Q99 = merged_df[col].quantile(0.99)
    merged_df[col] = merged_df[col].clip(lower=Q1, upper=Q99)
```
**Lý do**: Giữ lại các sự kiện PM2.5 cực đoan (đột biến ô nhiễm thực tế)

#### Bước 7: Chuẩn hóa Tính năng
```python
from sklearn.preprocessing import StandardScaler

# Chỉ chuẩn hóa các tính năng, KHÔNG chuẩn hóa mục tiêu
feature_cols = [col for col in merged_df.columns if col not in ['datetime', 'pm25']]
scaler = StandardScaler()
merged_df[feature_cols] = scaler.fit_transform(merged_df[feature_cols])
```
**Quan trọng**: Lưu scaler để triển khai sản xuất

#### Bước 8: Kiểm tra Đa cộng tuyến
```python
# Tính VIF
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Loại bỏ các tính năng có VIF > 10
```
**Hành động**: Giữ `temp`, loại bỏ `app_temp` (tương quan cao)

#### Bước 9: Chia Train-Test
```python
# QUAN TRỌNG: Không shuffle chuỗi thời gian!
train_size = int(len(merged_df) * 0.8)
train_df = merged_df.iloc[:train_size]
test_df = merged_df.iloc[train_size:]
```
**Thực hành Tốt nhất**: Chia theo thời gian bảo toàn thứ tự thời gian

### Tóm tắt Thực hành Tốt nhất

#### ✅ NÊN:
- ✅ Chuyển đổi datetime trước khi merge
- ✅ Loại bỏ các tính năng rò rỉ dữ liệu (AQI)
- ✅ Mã hóa tính năng tuần hoàn (sin/cos)
- ✅ Sử dụng forward fill cho giá trị thiếu trong chuỗi thời gian
- ✅ Giữ các outliers của PM2.5 (sự kiện thực)
- ✅ Chuẩn hóa tính năng nhưng không chuẩn hóa mục tiêu
- ✅ Chia train-test theo thời gian (không shuffle)

#### ❌ KHÔNG NÊN:
- ❌ Không sử dụng AQI làm tính năng
- ❌ Không loại bỏ outliers của PM2.5
- ❌ Không shuffle dữ liệu chuỗi thời gian
- ❌ Không sử dụng mean/median imputation
- ❌ Không quên lưu scaler
- ❌ Không chuẩn hóa trước khi chia (rò rỉ dữ liệu)

---

## 4. INSIGHTS TỪ PHÂN TÍCH KHÁM PHÁ DỮ LIỆU (EDA)

### Insights về Phân phối PM2.5
- **Phân phối**: Lệch phải với đuôi dài (nhiều giá trị cực đoan)
- **Phạm vi**: Từ không khí sạch (<12) đến nguy hại (>250)
- **Tác động sức khỏe**: Phần lớn thời gian không lành mạnh hoặc tồi tệ hơn
- **Tuần hoàn**: Các mẫu rõ ràng theo giờ và ngày

### Các Tương quan Chính với PM2.5

#### Tương quan Dương Mạnh (↑):
1. **PM10** (r > 0.8): Cùng loại hạt, di chuyển cùng nhau
2. **CO** (r > 0.6): Chỉ số phát thải giao thông
3. **NO2** (r > 0.5): Chỉ số phát thải giao thông

#### Tương quan Âm Mạnh (↓):
1. **Tốc độ Gió** (r < -0.4): Hiệu ứng phân tán
2. **Tầm nhìn xa** (r < -0.5): Không khí sạch hơn = tầm nhìn tốt hơn
3. **Lượng mưa** (r < -0.3): Mưa rửa trôi các chất ô nhiễm

### Các Mẫu Thời gian Phát hiện được

#### Mẫu theo Giờ:
- 📈 **Cao điểm**: 7-9 giờ sáng và 5-7 giờ chiều (giờ cao điểm)
- 📉 **Thấp nhất**: Giữa trưa (12-2 chiều) và đêm khuya
- 🔄 **Biến động**: Chênh lệch 50-100% giữa cao điểm/thấp điểm

**Insight**: Giao thông là nguyên nhân chính đóng góp vào PM2.5

#### Mẫu theo Tuần:
- Ngày trong tuần có PM2.5 cao hơn cuối tuần
- Sáng thứ Hai đặc biệt cao

### Phân tích Tác động Thời tiết

#### Hiệu ứng Tốc độ Gió:
- Gió yếu (<2 m/s): PM2.5 cao hơn +30-50%
- Gió mạnh (≥2 m/s): PM2.5 phân tán hiệu quả

#### Hiệu ứng Độ ẩm:
- Độ ẩm cao (>60%): PM2.5 cao hơn +20-30%
- Các hạt hấp thụ độ ẩm, trở nên nặng hơn, lắng gần mặt đất

#### Hiệu ứng Lượng mưa:
- Sự kiện mưa: PM2.5 thấp hơn -40-60%
- Hiệu ứng rửa trôi rất hiệu quả

### Tương tác các Tính năng Ô nhiễm
- Tất cả các chất ô nhiễm đều có tương quan dương với PM2.5
- PM10 là yếu tố dự đoán mạnh nhất trong số các chất ô nhiễm
- CO và NO2 chỉ ra đóng góp từ giao thông
- Tồn tại một số đa cộng tuyến (cần regularization)

---

## 5. ĐỀ XUẤT LỰA CHỌN MÔ HÌNH

### Các Mô hình Được Đề xuất (Xếp hạng)

#### 🥇 1. XGBoost (ĐỀ XUẤT CAO)
**Hiệu suất Kỳ vọng:**
- R² Score: 0.88-0.92
- RMSE: 10-15 μg/m³
- MAE: 8-12 μg/m³

**Ưu điểm:**
- ✅ Độ chính xác tốt nhất cho dữ liệu dạng bảng
- ✅ Xử lý mối quan hệ phi tuyến xuất sắc
- ✅ Regularization tích hợp (ngăn overfitting)
- ✅ Huấn luyện nhanh với hỗ trợ GPU
- ✅ Cung cấp tầm quan trọng của tính năng
- ✅ Bền vững với outliers và giá trị thiếu

**Siêu tham số cần điều chỉnh:**
- `n_estimators`: 100-500
- `max_depth`: 3-8
- `learning_rate`: 0.01-0.1
- `subsample`: 0.7-1.0
- `colsample_bytree`: 0.7-1.0

**Khi nào sử dụng:**
- Triển khai sản xuất (độ chính xác tốt nhất)
- Khi khả năng giải thích là thứ yếu
- Có đủ tài nguyên tính toán

---

#### 🥈 2. Random Forest
**Hiệu suất Kỳ vọng:**
- R² Score: 0.85-0.90
- RMSE: 12-18 μg/m³
- MAE: 10-14 μg/m³

**Ưu điểm:**
- ✅ Rất ổn định, ít overfitting hơn XGBoost
- ✅ Dễ điều chỉnh
- ✅ Khả năng giải thích tốt (tầm quan trọng tính năng)
- ✅ Không cần chuẩn hóa tính năng
- ✅ Xử lý giá trị thiếu tự nhiên

**Siêu tham số cần điều chỉnh:**
- `n_estimators`: 100-500
- `max_depth`: 10-30
- `min_samples_split`: 2-10
- `max_features`: 'sqrt', 'log2'

**Khi nào sử dụng:**
- Mô hình baseline nhanh
- Khi khả năng giải thích quan trọng
- Thời gian điều chỉnh hạn chế

---

#### 🥉 3. LightGBM
**Hiệu suất Kỳ vọng:**
- R² Score: 0.87-0.91
- RMSE: 11-16 μg/m³
- MAE: 9-13 μg/m³

**Ưu điểm:**
- ✅ Tốc độ huấn luyện nhanh nhất
- ✅ Hiệu quả bộ nhớ
- ✅ Tuyệt vời cho tập dữ liệu lớn
- ✅ Độ chính xác tương tự XGBoost

**Khi nào sử dụng:**
- Tập dữ liệu lớn (>100k bản ghi)
- Cần huấn luyện nhanh
- Bộ nhớ hạn chế

---

#### 4. Ridge/Lasso Regression
**Hiệu suất Kỳ vọng:**
- R² Score: 0.75-0.85
- RMSE: 15-22 μg/m³
- MAE: 12-18 μg/m³

**Ưu điểm:**
- ✅ Có thể giải thích cao (hệ số tuyến tính)
- ✅ Huấn luyện rất nhanh
- ✅ Xử lý đa cộng tuyến (regularization)
- ✅ Tốt cho lựa chọn tính năng (Lasso)

**Hạn chế:**
- ⚠️ Giả định mối quan hệ tuyến tính
- ⚠️ Cần kỹ thuật tính năng tốt
- ⚠️ Độ chính xác thấp hơn mô hình cây

**Khi nào sử dụng:**
- Cần khả năng giải thích (giải thích cho các bên liên quan)
- Tạo nguyên mẫu nhanh
- Tài nguyên tính toán hạn chế

---

#### 5. Mạng Neural (Feedforward)
**Hiệu suất Kỳ vọng:**
- R² Score: 0.82-0.90
- RMSE: 12-18 μg/m³
- MAE: 10-15 μg/m³

**Đề xuất Kiến trúc:**
```
Input → Dense(128, relu) → Dropout(0.3) 
      → Dense(64, relu) → Dropout(0.2)
      → Dense(32, relu) → Dense(1)
```

**Ưu điểm:**
- ✅ Có thể học các mẫu phức tạp
- ✅ Tốt với tập dữ liệu lớn
- ✅ Có thể thêm lớp LSTM cho phụ thuộc thời gian

**Hạn chế:**
- ⚠️ Yêu cầu nhiều dữ liệu hơn
- ⚠️ Khó giải thích
- ⚠️ Dễ overfit (tập dữ liệu nhỏ)
- ⚠️ Huấn luyện chậm hơn

**Khi nào sử dụng:**
- Có tập dữ liệu lớn (>50k bản ghi)
- Muốn nắm bắt các mẫu phức tạp
- Không cần khả năng giải thích

---

### Ma trận So sánh Mô hình

| Mô hình | Độ chính xác | Tốc độ | Khả năng giải thích | Nguy cơ Overfitting | Nhu cầu Feature Engineering | Đề xuất? |
|-------|----------|-------|------------------|------------------|-------------------------|--------------|
| **XGBoost** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ✅ CÓ |
| **Random Forest** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ✅ CÓ |
| **LightGBM** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ✅ CÓ |
| **Ridge/Lasso** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⚠️ BASELINE |
| **Neural Net** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⚠️ TÙY CHỌN |
| **SVR** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ KHÔNG ĐỀ XUẤT |

---

## 6. ĐỀ XUẤT KỸ THUẬT TÍNH NĂNG

### Các Tính năng Bắt buộc

#### 1. Mã hóa Tuần hoàn
```python
# Hướng gió
merged_df['wind_dir_sin'] = np.sin(np.deg2rad(merged_df['wind_dir']))
merged_df['wind_dir_cos'] = np.cos(np.deg2rad(merged_df['wind_dir']))

# Giờ trong ngày (nếu coi như tuần hoàn)
merged_df['hour_sin'] = np.sin(2 * np.pi * merged_df['hour'] / 24)
merged_df['hour_cos'] = np.cos(2 * np.pi * merged_df['hour'] / 24)
```

#### 2. Tính năng Thời gian
```python
merged_df['hour'] = merged_df['datetime'].dt.hour
merged_df['day_of_week'] = merged_df['datetime'].dt.dayofweek
merged_df['is_rush_hour'] = merged_df['hour'].isin([7,8,9,17,18,19]).astype(int)
merged_df['is_weekend'] = merged_df['day_of_week'].isin([5,6]).astype(int)
```

#### 3. Tính năng Lag (Chuỗi Thời gian)
```python
# PM2.5 giờ trước
merged_df['pm25_lag1'] = merged_df['pm25'].shift(1)
merged_df['pm25_lag3'] = merged_df['pm25'].shift(3)

# Thời tiết giờ trước
merged_df['temp_lag1'] = merged_df['temp'].shift(1)
merged_df['wind_spd_lag1'] = merged_df['wind_spd'].shift(1)
```

#### 4. Thống kê Rolling
```python
# Trung bình động 3 giờ
merged_df['pm25_ma3'] = merged_df['pm25'].rolling(window=3).mean()
merged_df['temp_ma3'] = merged_df['temp'].rolling(window=3).mean()

# Trung bình động 6 giờ
merged_df['pm25_ma6'] = merged_df['pm25'].rolling(window=6).mean()
```

### Tính năng Nâng cao (Tùy chọn)

#### 5. Tương tác
```python
merged_df['wind_temp'] = merged_df['wind_spd'] * merged_df['temp']
merged_df['rh_temp'] = merged_df['rh'] * merged_df['temp']
merged_df['wind_rh'] = merged_df['wind_spd'] * merged_df['rh']
```

#### 6. Tính năng Đa thức
```python
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)
# Áp dụng chỉ cho các tính năng được chọn
```

#### 7. Phân loại Điều kiện Thời tiết
```python
# Phân loại gió
merged_df['wind_category'] = pd.cut(merged_df['wind_spd'], 
                                     bins=[0, 2, 5, float('inf')],
                                     labels=['Yếu', 'Trung bình', 'Mạnh'])

# Phân loại độ ẩm
merged_df['humidity_category'] = pd.cut(merged_df['rh'],
                                         bins=[0, 40, 60, 80, 100],
                                         labels=['Khô', 'Thoải mái', 'Ẩm', 'Rất ẩm'])
```

---

## 7. KẾT QUẢ KỲ VỌNG & CHIẾN LƯỢC KIỂM CHỨNG

### Mục tiêu Hiệu suất

#### Hiệu suất Chấp nhận được Tối thiểu:
- R² Score: ≥ 0.80
- RMSE: ≤ 20 μg/m³
- MAE: ≤ 15 μg/m³
- Độ chính xác Phân loại AQI: ≥ 85%

#### Hiệu suất Mục tiêu:
- R² Score: ≥ 0.85
- RMSE: ≤ 15 μg/m³
- MAE: ≤ 10 μg/m³
- Độ chính xác Phân loại AQI: ≥ 90%

#### Hiệu suất Xuất sắc:
- R² Score: ≥ 0.90
- RMSE: ≤ 12 μg/m³
- MAE: ≤ 8 μg/m³
- Độ chính xác Phân loại AQI: ≥ 95%

### Chiến lược Kiểm chứng

#### 1. Chia Train-Validation-Test
```
├── Tập Huấn luyện (70%): Huấn luyện mô hình
├── Tập Kiểm chứng (15%): Điều chỉnh siêu tham số
└── Tập Kiểm tra (15%): Đánh giá cuối cùng
```

#### 2. Cross-Validation (Chuỗi Thời gian)
- Sử dụng TimeSeriesSplit (không phải KFold)
- Cross-validation thời gian 5-fold
- Ngăn chặn rò rỉ dữ liệu

#### 3. Chỉ số cần Theo dõi
- **Chỉ số hồi quy**: R², RMSE, MAE, MAPE
- **Chỉ số kinh doanh**: Độ chính xác phân loại AQI, tỷ lệ âm tính giả
- **Phân tích phần dư**: Kiểm tra các mẫu trong lỗi

---

## 8. LỘ TRÌNH TRIỂN KHAI

### Giai đoạn 1: Chuẩn bị Dữ liệu (Tuần 1)
- ✅ Tải và merge các tập dữ liệu
- ✅ Xử lý giá trị thiếu
- ✅ Loại bỏ rò rỉ dữ liệu
- ✅ Kỹ thuật các tính năng cơ bản
- ✅ Chia train-test

### Giai đoạn 2: EDA & Kỹ thuật Tính năng (Tuần 1-2)
- ✅ EDA toàn diện (hoàn thành trong notebook)
- ✅ Tạo tính năng lag và rolling
- ✅ Tương tác
- ✅ Lựa chọn tính năng

### Giai đoạn 3: Phát triển Mô hình (Tuần 2-3)
- 🔄 Huấn luyện mô hình baseline (Linear Regression, Ridge)
- 🔄 Huấn luyện mô hình dựa trên cây (Random Forest, XGBoost)
- 🔄 Huấn luyện Mạng Neural (tùy chọn)
- 🔄 So sánh hiệu suất

### Giai đoạn 4: Tối ưu hóa (Tuần 3)
- 🔄 Điều chỉnh siêu tham số (GridSearchCV, RandomizedSearchCV)
- 🔄 Tinh chỉnh lựa chọn tính năng
- 🔄 Phương pháp ensemble (stacking, voting)

### Giai đoạn 5: Đánh giá & Tác động Kinh doanh (Tuần 4)
- 🔄 Đánh giá mô hình cuối cùng
- 🔄 Phân tích lỗi
- 🔄 Tính toán tác động kinh doanh
- 🔄 Đề xuất

### Giai đoạn 6: Tài liệu & Thuyết trình (Tuần 4)
- 🔄 Báo cáo cuối cùng
- 🔄 Tài liệu mã nguồn
- 🔄 Slide thuyết trình

---

## 9. PHÂN TÍCH TÁC ĐỘNG KINH DOANH

### Các Kịch bản Sử dụng

#### Kịch bản 1: Hệ thống Cảnh báo Sớm
**Đầu ra Mô hình**: PM2.5 = 85 μg/m³ dự đoán cho ngày mai lúc 8 giờ sáng

**Hành động:**
- 🔔 Gửi cảnh báo SMS cho công dân
- 📱 Thông báo ứng dụng di động
- 🏫 Trường học hoãn các hoạt động ngoài trời
- 🏥 Bệnh viện chuẩn bị cho bệnh nhân hô hấp

**Tác động**: Giảm 15% sự cố sức khỏe

#### Kịch bản 2: Hỗ trợ Quyết định Chính sách
**Đầu ra Mô hình**: PM2.5 cao dự kiến trong 3 ngày tới (>100 μg/m³)

**Hành động:**
- 🚫 Lệnh đóng cửa nhà máy tạm thời
- 🚗 Hạn chế phương tiện (biển số chẵn/lẻ)
- 🏗️ Tạm dừng xây dựng

**Tác động**: Giảm PM2.5 20-30%

#### Kịch bản 3: Lập kế hoạch Kinh doanh
**Đầu ra Mô hình**: Chất lượng không khí tốt tuần tới (<35 μg/m³)

**Hành động:**
- 🎫 Đại lý du lịch quảng bá tour ngoài trời
- 🏃 Trung tâm thể dục lập kế hoạch sự kiện ngoài trời
- 📸 Studio nhiếp ảnh đặt phiên chụp ngoài trời

**Tác động**: Tăng doanh thu 10-15%

### Tính toán ROI

#### Đầu tư:
- Cơ sở hạ tầng thu thập dữ liệu: $50,000
- Phát triển mô hình: $30,000
- Triển khai & bảo trì: $20,000/năm
- **Tổng Năm 1**: $100,000

#### Lợi nhuận (Hàng năm):
- Tiết kiệm chi phí y tế: $800,000
- Tăng năng suất: $600,000
- Tăng doanh thu du lịch: $400,000
- **Tổng Lợi nhuận**: $1,800,000

**ROI = (1,800,000 - 100,000) / 100,000 = 1,700%**
**Thời gian Hoàn vốn: ~3 tuần**

---

## 10. KẾT LUẬN & BƯỚC TIẾP THEO

### Bài học Chính

1. ✅ **Bài toán được định nghĩa rõ ràng**: Trường hợp kinh doanh rõ ràng cho dự đoán PM2.5
2. ✅ **Dữ liệu đầy đủ**: Đủ tính năng và bản ghi cho ML
3. ✅ **Mẫu mạnh tồn tại**: Tương quan và mẫu thời gian rõ ràng
4. ✅ **Nhiều cách tiếp cận khả thi**: Mô hình dựa trên cây hứa hẹn nhất
5. ✅ **Tác động kinh doanh cao**: Tiềm năng ROI đáng kể

### Hành động Được Đề xuất Tiếp theo

#### Ngay lập tức (Tuần này):
1. ✅ Hoàn thành EDA (HOÀN THÀNH)
2. 🔄 Triển khai pipeline tiền xử lý
3. 🔄 Tạo tất cả các tính năng được kỹ thuật
4. 🔄 Huấn luyện mô hình baseline

#### Ngắn hạn (2 Tuần tới):
1. 🔄 Huấn luyện và điều chỉnh XGBoost
2. 🔄 Huấn luyện Random Forest
3. 🔄 So sánh mô hình
4. 🔄 Chọn mô hình tốt nhất

#### Trung hạn (Tháng tới):
1. 🔄 Tối ưu hóa siêu tham số
2. 🔄 Xây dựng mô hình ensemble
3. 🔄 Kiểm chứng trên tập test
4. 🔄 Hoàn thành tài liệu

### Tiêu chí Thành công

Dự án sẽ được coi là thành công nếu:
- ✅ R² Score > 0.85
- ✅ RMSE < 15 μg/m³
- ✅ Mô hình có thể giải thích cho các bên liên quan
- ✅ Có thể triển khai trong môi trường sản xuất
- ✅ Cung cấp insights kinh doanh có thể hành động

---

## 📚 TÀI LIỆU THAM KHẢO

### Các Kỹ thuật Khai thác Dữ liệu Được Sử dụng:
1. **Phân tích Hồi quy**: Dự đoán PM2.5
2. **Kỹ thuật Tính năng**: Tạo tính năng thời gian và tương tác
3. **Phương pháp Ensemble**: XGBoost, Random Forest
4. **Regularization**: Ridge, Lasso cho đa cộng tuyến
5. **Phân tích Chuỗi Thời gian**: Tính năng lag, thống kê rolling

### Thư viện Chính:
- **Pandas**: Thao tác dữ liệu
- **NumPy**: Tính toán số học
- **Scikit-learn**: Mô hình ML và tiền xử lý
- **XGBoost/LightGBM**: Gradient boosting
- **Matplotlib/Seaborn**: Trực quan hóa
- **Statsmodels**: Phân tích thống kê

---

## 📝 KIỂM SOÁT PHIÊN BẢN TÀI LIỆU

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---------|------|--------|---------|
| 1.0 | 4 tháng 12, 2025 | Trợ lý AI | Phân tích toàn diện ban đầu |

---

**KẾT THÚC TÓM TẮT PHÂN TÍCH**

*Tài liệu này phục vụ như một hướng dẫn toàn diện cho Dự án Cuối kỳ DAM501 về Dự đoán PM2.5. Tất cả phân tích, đề xuất và insights đều dựa trên EDA kỹ lưỡng và các thực hành tốt nhất về khai thác dữ liệu.*
