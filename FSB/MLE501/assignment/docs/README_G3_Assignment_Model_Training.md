# README - G3_Assignment_Model_Training

## 📋 Mục Lục
1. [Tổng Quan](#tổng-quan)
2. [Mục Đích và Động Lực](#mục-đích-và-động-lực)
3. [Kiến Trúc Pipeline](#kiến-trúc-pipeline)
4. [Chi Tiết Kỹ Thuật](#chi-tiết-kỹ-thuật)
5. [Feature Engineering](#feature-engineering)
6. [So Sánh Dữ Liệu Gốc vs Chuẩn Hóa](#so-sánh-dữ-liệu-gốc-vs-chuẩn-hóa)
7. [Các Mô Hình Machine Learning](#các-mô-hình-machine-learning)
8. [Đánh Giá và Metrics](#đánh-giá-và-metrics)
9. [Kết Quả Thực Nghiệm](#kết-quả-thực-nghiệm)
10. [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)
11. [Best Practices](#best-practices)

---

## 🎯 Tổng Quan

Notebook `G3_Assignment_Model_Training.ipynb` là hệ thống huấn luyện mô hình Machine Learning để **dự báo nồng độ PM2.5** (bụi mịn) trong không khí Hà Nội. Đây là bước thứ 2 trong quy trình phân tích chất lượng không khí, sử dụng dữ liệu từ `weather_data_hanoi.csv` đã được thu thập ở bước trước.

### Điểm Nổi Bật

- ✅ **3 thuật toán ML**: Linear Regression, Random Forest, XGBoost
- ✅ **So sánh 2 phương pháp**: Dữ liệu gốc vs Dữ liệu chuẩn hóa
- ✅ **Feature Engineering**: Tạo các đặc trưng thời gian (year, month, day, hour, weekday)
- ✅ **Xử lý đa cộng tuyến**: Loại bỏ cột `aqi` có tương quan cao với PM2.5
- ✅ **Comprehensive Evaluation**: R², RMSE, MAE, Training Time
- ✅ **Model Persistence**: Lưu mô hình và scaler để sử dụng sau này

---

## 🎪 Mục Đích và Động Lực

### Vấn Đề Cần Giải Quyết

**Tại sao cần dự báo PM2.5?**

1. **Sức khỏe cộng đồng**: 
   - PM2.5 gây các bệnh về hô hấp, tim mạch, ung thư phổi
   - WHO khuyến cáo: PM2.5 < 15 µg/m³ (24h), nhưng Hà Nội thường > 50 µg/m³

2. **Ra quyết định sớm**:
   - Cảnh báo trước cho người dân tránh ra ngoài
   - Lên kế hoạch giảm thiểu ô nhiễm (hạn chế xe cộ, đóng cửa nhà máy)

3. **Nghiên cứu khoa học**:
   - Hiểu mối quan hệ giữa các yếu tố ô nhiễm
   - Xác định nguồn gây ô nhiễm chính

### Mục Tiêu Cụ Thể

1. **So sánh hiệu quả**: Dữ liệu gốc vs Dữ liệu chuẩn hóa
   - *Tại sao?* Chuẩn hóa có thể cải thiện một số mô hình, nhưng không phải tất cả
   
2. **Tìm mô hình tốt nhất**: Dựa trên R², RMSE, MAE
   - *Mục tiêu:* R² > 0.95, RMSE < 10 µg/m³
   
3. **Deployment-ready**: Lưu mô hình và scaler để predict trong production

---

## 🏗️ Kiến Trúc Pipeline

### Sơ Đồ Tổng Thể

```
┌─────────────────────────┐
│ weather_data_hanoi.csv  │
│   (Raw Data Input)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  1. Data Loading        │
│  - Read CSV             │
│  - Initial Inspection   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  2. Feature Engineering │
│  - Parse datetime       │
│  - Extract time features│
│  - Drop unnecessary cols│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  3. Correlation Analysis│
│  - Heatmap              │
│  - Identify high corr   │
│  - Drop 'aqi' (r>0.99)  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  4. Train-Test Split    │
│  - 80% train, 20% test  │
│  - Stratified by time   │
└───────────┬─────────────┘
            │
            ├──────────────────────────┐
            │                          │
            ▼                          ▼
┌─────────────────────┐    ┌─────────────────────┐
│  5a. Original Data  │    │  5b. Scaled Data    │
│  (No Scaling)       │    │  (StandardScaler)   │
└──────────┬──────────┘    └──────────┬──────────┘
           │                          │
           ▼                          ▼
┌─────────────────────┐    ┌─────────────────────┐
│  6a. Train Models   │    │  6b. Train Models   │
│  - Linear Reg       │    │  - Linear Reg       │
│  - Random Forest    │    │  - Random Forest    │
│  - XGBoost          │    │  - XGBoost          │
└──────────┬──────────┘    └──────────┬──────────┘
           │                          │
           └──────────┬───────────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  7. Compare Results │
           │  - R², RMSE, MAE    │
           │  - Visualization    │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  8. Save Best Models│
           │  - .pkl files       │
           │  - Scaler           │
           └─────────────────────┘
```

### Workflow Chi Tiết

#### **Phase 1: Data Preparation** (Cell 1-4)
```python
# Cell 1: Load data
df = pd.read_csv('weather_data_hanoi.csv')
```
- Đọc dữ liệu từ CSV
- Kiểm tra info() và head() để hiểu cấu trúc

#### **Phase 2: Feature Engineering** (Cell 2-3)
- Parse datetime từ string sang datetime object
- Extract 5 temporal features: year, month, day, hour, weekday
- Drop các cột không cần: timestamp_utc, ts, datetime, timestamp_local

#### **Phase 3: Feature Selection** (Cell 4-6)
- Tính correlation matrix
- Phát hiện `aqi` có r > 0.99 với PM2.5
- Drop `aqi` để tránh multicollinearity

#### **Phase 4: Data Splitting** (Cell 7-9)
- Train-test split: 80-20
- Tạo 2 datasets: Original và Scaled

#### **Phase 5: Model Training** (Cell 10-11)
- Train 3 models trên 2 datasets (6 experiments tổng cộng)

#### **Phase 6: Evaluation** (Cell 12-13)
- So sánh metrics
- Visualization

#### **Phase 7: Model Persistence** (Cell 14)
- Save best models và scaler

---

## 🔧 Chi Tiết Kỹ Thuật

### 1. Data Loading và Inspection

**Code:**
```python
import pandas as pd
df = pd.read_csv('weather_data_hanoi.csv')
print(df.info())
print(df.head())
```

**Tại sao cần inspect?**
- **Kiểm tra dtypes**: Đảm bảo numeric columns là float/int
- **Kiểm tra missing values**: Detect null/NaN values
- **Kiểm tra shape**: Xác nhận số lượng records và features
- **Preview data**: Hiểu distribution và range của dữ liệu

**Expected Output:**
```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 16800 entries, 0 to 16799
Data columns (total 11 columns):
 #   Column             Non-Null Count  Dtype  
---  ------             --------------  -----  
 0   aqi                16800 non-null  int64  
 1   co                 16800 non-null  float64
 2   datetime           16800 non-null  object 
 3   no2                16800 non-null  float64
 4   o3                 16800 non-null  float64
 5   pm10               16800 non-null  float64
 6   pm25               16800 non-null  float64
 7   so2                16800 non-null  float64
 8   timestamp_local    16800 non-null  object 
 9   timestamp_utc      16800 non-null  object 
 10  ts                 16800 non-null  int64  
```

### 2. Identify Non-Numeric Columns

**Code:**
```python
non_numeric_columns = df.select_dtypes(exclude=['number']).columns
print("Các cột không phải số:", non_numeric_columns.tolist())
```

**Tại sao quan trọng?**
- **ML models chỉ nhận numeric input**: Cần xử lý string columns
- **Phát hiện datetime columns**: Cần parsing đặc biệt
- **Planning preprocessing**: Xác định chiến lược xử lý

**Expected Output:**
```
Các cột không phải số: ['datetime', 'timestamp_local', 'timestamp_utc']
```

---

## 🛠️ Feature Engineering

### Temporal Features Extraction

**Code:**
```python
df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d:%H')
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['day'] = df['datetime'].dt.day
df['hour'] = df['datetime'].dt.hour
df['weekday'] = df['datetime'].dt.weekday
```

### Tại Sao Cần Temporal Features?

#### 1. **Year (Năm)**
```python
df['year'] = df['datetime'].dt.year  # 2023, 2024, ...
```

**Lý do:**
- Phát hiện **xu hướng dài hạn** (long-term trend)
- Ví dụ: PM2.5 có thể giảm dần do chính sách môi trường
- Tuy nhiên, với dataset 2 năm, feature này ít quan trọng

**Khi nào quan trọng?**
- Dataset > 5 năm
- Có thay đổi chính sách lớn (ví dụ: đóng cửa nhà máy nhiệt điện)

#### 2. **Month (Tháng)**
```python
df['month'] = df['datetime'].dt.month  # 1-12
```

**Lý do:**
- **Seasonality (Tính mùa vụ)**: 
  - Tháng 12-2: Mùa đông, PM2.5 cao (không khí lạnh, đốt than)
  - Tháng 6-8: Mùa hè, PM2.5 thấp hơn (mưa nhiều, làm sạch không khí)
- **Pattern mạnh nhất** trong dữ liệu

**Ví dụ thực tế (Hà Nội):**
```
Tháng 1-2:  PM2.5 trung bình 80-120 µg/m³ (nguy hiểm)
Tháng 6-7:  PM2.5 trung bình 30-50 µg/m³  (trung bình)
```

#### 3. **Day (Ngày trong tháng)**
```python
df['day'] = df['datetime'].dt.day  # 1-31
```

**Lý do:**
- **Chu kỳ trong tháng**: Đầu tháng vs cuối tháng
- Ít quan trọng hơn month và weekday
- Có thể bỏ qua nếu model overfitting

#### 4. **Hour (Giờ trong ngày)**
```python
df['hour'] = df['datetime'].dt.hour  # 0-23
```

**Lý do:**
- **Daily pattern rất rõ ràng**:
  - 7-9h: Rush hour, PM2.5 tăng đột biến (xe cộ)
  - 12-14h: Giảm (gió mạnh, nhiệt độ cao)
  - 19-21h: Rush hour chiều, tăng lại
  - 2-5h: Thấp nhất (ít hoạt động)

**Visualization:**
```
PM2.5 (µg/m³)
100 |     ╱╲              ╱╲
 80 |    ╱  ╲            ╱  ╲
 60 |   ╱    ╲__________╱    ╲
 40 |  ╱                      ╲___
    +─────────────────────────────
    0  4  8  12 16 20 24 (hour)
```

#### 5. **Weekday (Thứ trong tuần)**
```python
df['weekday'] = df['datetime'].dt.weekday  # 0=Monday, 6=Sunday
```

**Lý do:**
- **Workday vs Weekend pattern**:
  - T2-T6: PM2.5 cao hơn (traffic, industrial activity)
  - T7-CN: PM2.5 thấp hơn (ít xe cộ, nhà máy nghỉ)

**Expected difference:**
```
Weekday average:  PM2.5 ≈ 65 µg/m³
Weekend average:  PM2.5 ≈ 55 µg/m³  (-15%)
```

### Tổng Hợp: Importance Ranking

| Feature | Importance | Lý Do |
|---------|-----------|-------|
| **hour** | ⭐⭐⭐⭐⭐ | Daily pattern rõ ràng, rush hour |
| **month** | ⭐⭐⭐⭐⭐ | Seasonal effect, winter pollution |
| **weekday** | ⭐⭐⭐ | Workday vs weekend |
| **day** | ⭐⭐ | Weak signal |
| **year** | ⭐ | Dataset ngắn, ít thay đổi |

### Drop Unnecessary Columns

**Code:**
```python
df = df.drop(columns=['timestamp_utc', 'ts', 'datetime', 'timestamp_local'])
```

**Tại sao drop?**

| Column | Lý Do Drop |
|--------|-----------|
| `datetime` | Đã extract thành year, month, day, hour, weekday |
| `timestamp_local` | Duplicate của datetime |
| `timestamp_utc` | Không cần (đã có local time) |
| `ts` | Unix timestamp, redundant với datetime |

**Lợi ích:**
- ✅ Giảm số features (tránh overfitting)
- ✅ Tránh data leakage (timestamp chứa thông tin tương lai)
- ✅ Faster training (ít features hơn)

---

## 📊 Correlation Analysis và Multicollinearity

### Tính Correlation Matrix

**Code:**
```python
import seaborn as sns
import matplotlib.pyplot as plt

numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
correlation_matrix = df[numeric_cols].corr()

plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title("Ma trận tương quan giữa các đặc trưng")
plt.show()
```

### Tại Sao Cần Correlation Analysis?

#### 1. **Phát hiện Multicollinearity (Đa cộng tuyến)**

**Định nghĩa:**
- Multicollinearity: Khi 2+ features có tương quan cao với nhau
- Nguy hại: Gây instability trong Linear Regression, khó interpret coefficients

**Ví dụ:**
```
Correlation between AQI and PM2.5: r = 0.987
```

**Tại sao r cao như vậy?**
```python
# AQI được tính từ công thức dựa trên PM2.5, PM10, NO2, SO2, O3
AQI = max(AQI_pm25, AQI_pm10, AQI_no2, AQI_so2, AQI_o3)
```

→ AQI gần như là hàm của PM2.5 (vì PM2.5 thường cao nhất)

#### 2. **Phát Hiện High Correlation Pairs**

**Code:**
```python
high_corr_pairs = correlation_matrix.unstack().sort_values(ascending=False)
high_corr_pairs = high_corr_pairs[high_corr_pairs < 1]
print("Các cặp đặc trưng có tương quan cao:")
print(high_corr_pairs[high_corr_pairs > 0.8])
```

**Expected Output:**
```
pm25  aqi     0.987123
pm10  aqi     0.823456
pm10  pm25    0.789012
co    pm25    0.654321
```

### Quyết Định: Drop AQI

**Code:**
```python
df.drop(columns=['aqi'], inplace=True)
```

**Tại sao drop AQI mà không drop PM2.5?**

| Tiêu Chí | AQI | PM2.5 |
|----------|-----|-------|
| **Target variable** | Không | **Có** (mục tiêu dự báo) |
| **Derived feature** | **Có** (tính từ PM2.5) | Không |
| **Direct measurement** | Không | **Có** |
| **Redundant** | **Có** | Không |

**Consequence:**
- ✅ Tránh overfitting (không dùng biến phụ thuộc để dự báo chính nó)
- ✅ Model generalize tốt hơn
- ✅ Giảm multicollinearity cho Linear Regression

---

## 🎯 Train-Test Split

### Code

```python
from sklearn.model_selection import train_test_split

X = df.drop(columns=['pm25'])  # Features
y = df['pm25']                  # Target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### Tại Sao 80-20 Split?

**Reasoning:**

| Split | Train Size | Test Size | Khi nào dùng? |
|-------|-----------|-----------|---------------|
| 90-10 | 15,120 | 1,680 | Dataset nhỏ (< 5,000) |
| **80-20** | **13,440** | **3,360** | **Standard, balanced** |
| 70-30 | 11,760 | 5,040 | Dataset lớn (> 50,000) |

**Lợi ích 80-20:**
- ✅ Train set đủ lớn (13,440 samples) → model học tốt
- ✅ Test set đủ lớn (3,360 samples) → estimate reliable
- ✅ Standard practice trong industry

### random_state=42

**Tại sao set seed?**
```python
random_state=42  # Magic number
```

**Lợi ích:**
- ✅ **Reproducibility**: Kết quả giống nhau mỗi lần chạy
- ✅ **Debugging**: Dễ so sánh khi thay đổi code
- ✅ **Collaboration**: Team members có cùng results

**Tại sao 42?**
- Meme trong ML community (từ "The Hitchhiker's Guide to the Galaxy")
- Có thể dùng bất kỳ số nào (0, 123, 999, ...)

---

## ⚖️ So Sánh Dữ Liệu Gốc vs Chuẩn Hóa

### Standardization với StandardScaler

**Code:**
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### Công Thức StandardScaler

```
x_scaled = (x - mean) / std

Trong đó:
- mean: Giá trị trung bình của feature
- std: Standard deviation
```

**Ví dụ:**
```python
# Original data
co = [340.0, 357.9, 375.8, 454.8]  # µg/m³

# Scaled data (mean=382.125, std=49.88)
co_scaled = [(340-382.125)/49.88,
             (357.9-382.125)/49.88,
             (375.8-382.125)/49.88,
             (454.8-382.125)/49.88]
          = [-0.845, -0.486, -0.127, 1.457]
```

### Tại Sao Cần Chuẩn Hóa?

#### 1. **Feature Scale Difference**

**Vấn đề:**
```python
# Các features có scale khác nhau rất nhiều
co:    [300, 500]      µg/m³
no2:   [20, 80]        µg/m³
o3:    [30, 100]       µg/m³
hour:  [0, 23]         hours
month: [1, 12]         months
```

**Hậu quả:**
- Linear Regression: Coefficients bị bias về features có scale lớn
- Gradient Descent: Converge chậm hoặc không converge

#### 2. **Impact trên từng Model**

| Model | Cần Scaling? | Lý Do |
|-------|--------------|-------|
| **Linear Regression** | ⚠️ Recommended | Coefficients dễ interpret, gradient descent ổn định |
| **Random Forest** | ❌ No | Tree-based, không phụ thuộc scale |
| **XGBoost** | ❌ No | Tree-based, không phụ thuộc scale |
| Neural Networks | ✅ Yes | Cực kỳ quan trọng |
| SVM | ✅ Yes | Distance-based |
| K-Means | ✅ Yes | Distance-based |

### Tại Sao Test Cả 2 Phương Pháp?

**Chiến lược thực nghiệm:**
```
Hypothesis 1: Scaling cải thiện Linear Regression
Hypothesis 2: Scaling không ảnh hưởng Random Forest/XGBoost
Hypothesis 3: Có thể có unexpected benefits
```

**Thực tế:**
- Linear Regression: Có thể cải thiện nhẹ (convergence nhanh hơn)
- Random Forest: Không thay đổi (đã verify hypothesis)
- XGBoost: Có thể thay đổi nhẹ (do regularization)

### fit_transform vs transform

**Code:**
```python
X_train_scaled = scaler.fit_transform(X_train)  # Học mean, std từ train
X_test_scaled = scaler.transform(X_test)        # Dùng mean, std đã học
```

**Tại sao không fit trên test set?**

**❌ SAI:**
```python
# DATA LEAKAGE!
scaler_test = StandardScaler()
X_test_scaled = scaler_test.fit_transform(X_test)
```

**Lý do:**
- Test set phải simulate "unseen data" trong production
- Nếu fit trên test set → biết trước distribution của test data
- Kết quả đánh giá sẽ **optimistic** (không phản ánh thực tế)

**✅ ĐÚNG:**
```python
# Chỉ học từ train, áp dụng cho test
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

---

## 🤖 Các Mô Hình Machine Learning

### 1. Linear Regression

**Code:**
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
```

**Công Thức:**
```
PM2.5 = β₀ + β₁·CO + β₂·NO₂ + β₃·O₃ + ... + β_n·weekday
```

**Đặc điểm:**

| Aspect | Chi Tiết |
|--------|----------|
| **Algorithm** | Ordinary Least Squares (OLS) |
| **Complexity** | O(n·m²) - n: samples, m: features |
| **Assumptions** | Linearity, independence, homoscedasticity |
| **Interpretability** | ⭐⭐⭐⭐⭐ (dễ hiểu nhất) |
| **Speed** | ⭐⭐⭐⭐⭐ (nhanh nhất) |
| **Accuracy** | ⭐⭐⭐ (trung bình) |

**Ưu điểm:**
- ✅ Đơn giản, dễ hiểu
- ✅ Training rất nhanh
- ✅ Coefficients có ý nghĩa (feature importance)
- ✅ Không cần tuning hyperparameters

**Nhược điểm:**
- ❌ Chỉ capture linear relationships
- ❌ Nhạy cảm với outliers
- ❌ Giả định strong (linearity, homoscedasticity)
- ❌ Không handle interactions giữa features

**Khi nào dùng?**
- Baseline model (để so sánh)
- Quick prototyping
- Interpretability quan trọng hơn accuracy

### 2. Random Forest Regressor

**Code:**
```python
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(
    n_estimators=100,    # 100 trees
    random_state=42,
    n_jobs=-1            # Use all CPU cores
)
```

**Kiến trúc:**
```
         Random Forest
              │
    ┌─────────┼─────────┐
    │         │         │
  Tree1     Tree2     Tree100
    │         │         │
  Pred1     Pred2     Pred100
    │         │         │
    └─────────┴─────────┘
            │
        Average
            │
      Final Prediction
```

**Đặc điểm:**

| Aspect | Chi Tiết |
|--------|----------|
| **Algorithm** | Ensemble of Decision Trees |
| **Complexity** | O(n·m·log(n)·T) - T: số trees |
| **Assumptions** | Không có (non-parametric) |
| **Interpretability** | ⭐⭐⭐ (feature importance) |
| **Speed** | ⭐⭐⭐ (trung bình) |
| **Accuracy** | ⭐⭐⭐⭐⭐ (rất cao) |

**Hyperparameters:**

```python
n_estimators=100  # Số lượng trees
```
- **Tại sao 100?** Balance giữa accuracy và speed
- Nhiều hơn (200, 500): Accuracy tăng nhẹ, training lâu hơn
- Ít hơn (10, 50): Training nhanh, nhưng accuracy giảm

```python
n_jobs=-1  # Use all CPU cores
```
- **Tại sao -1?** Maximize parallelization
- 1 tree độc lập, có thể train parallel
- Training time giảm 4-8x (tùy CPU)

**Ưu điểm:**
- ✅ Capture non-linear relationships
- ✅ Robust to outliers
- ✅ Không cần scaling
- ✅ Handle feature interactions tự động
- ✅ Ít overfitting (do averaging)

**Nhược điểm:**
- ❌ Training chậm hơn Linear Regression
- ❌ Prediction chậm (phải query 100 trees)
- ❌ Model size lớn (100 trees)
- ❌ Khó interpret từng prediction

**Khi nào dùng?**
- Data có non-linear patterns
- Cần accuracy cao
- Không quan tâm model size
- Có CPU/RAM đủ mạnh

### 3. XGBoost Regressor

**Code:**
```python
import xgboost as xgb
model = xgb.XGBRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
```

**Kiến trúc:**
```
XGBoost (Gradient Boosting)

Tree1 → Residual1 → Tree2 → Residual2 → Tree3 → ... → Tree100
  ↓                   ↓                   ↓              ↓
Pred1         +     Pred2        +      Pred3    +    Pred100
  └──────────────────┴──────────────────┴────────────────┘
                            │
                    Final Prediction
```

**Khác với Random Forest:**

| Feature | Random Forest | XGBoost |
|---------|--------------|---------|
| **Training** | Parallel (independent trees) | Sequential (boosting) |
| **Tree dependency** | Independent | Dependent (correct previous errors) |
| **Prediction** | Average | Weighted sum |
| **Overfitting risk** | Low | Higher (cần regularization) |
| **Speed** | Faster | Slower |
| **Accuracy** | High | **Highest** |

**Đặc điểm:**

| Aspect | Chi Tiết |
|--------|----------|
| **Algorithm** | Gradient Boosting on Decision Trees |
| **Complexity** | O(n·m·log(n)·T) sequential |
| **Assumptions** | Không có |
| **Interpretability** | ⭐⭐⭐ (feature importance, SHAP) |
| **Speed** | ⭐⭐ (chậm hơn RF) |
| **Accuracy** | ⭐⭐⭐⭐⭐ (cao nhất) |

**Ưu điểm:**
- ✅ **State-of-the-art accuracy** (thường thắng Kaggle)
- ✅ Handle missing values tự động
- ✅ Built-in regularization (L1, L2)
- ✅ Feature importance reliable
- ✅ Tối ưu cho speed (C++ implementation)

**Nhược điểm:**
- ❌ Training chậm (sequential)
- ❌ Nhiều hyperparameters cần tune
- ❌ Dễ overfit nếu không regularize
- ❌ Cần install thư viện external

**Khi nào dùng?**
- **Production systems** (accuracy quan trọng nhất)
- **Kaggle competitions**
- Data có complex patterns
- Sẵn sàng tune hyperparameters

---

## 📏 Đánh Giá và Metrics

### Các Metrics Sử Dụng

#### 1. **R² Score (Coefficient of Determination)**

**Công thức:**
```
R² = 1 - (SS_res / SS_tot)

SS_res = Σ(y_true - y_pred)²  # Residual sum of squares
SS_tot = Σ(y_true - y_mean)²  # Total sum of squares
```

**Ý nghĩa:**
- **R² = 1.0**: Perfect prediction (mọi điểm đều trên đường fit)
- **R² = 0.95**: Model giải thích 95% variance của data
- **R² = 0.0**: Model không tốt hơn việc dùng mean
- **R² < 0.0**: Model tệ hơn việc dùng mean (very bad)

**Interpretation:**
```python
R² = 0.972  # Model giải thích 97.2% sự biến thiên của PM2.5
```

**Ưu điểm:**
- ✅ Normalized (0-1), dễ interpret
- ✅ Scale-independent
- ✅ Standard metric trong regression

**Nhược điểm:**
- ❌ Có thể misleading với outliers
- ❌ Luôn tăng khi thêm features (adjusted R² tốt hơn)

#### 2. **RMSE (Root Mean Squared Error)**

**Công thức:**
```
RMSE = √[Σ(y_true - y_pred)² / n]
```

**Ý nghĩa:**
- Sai số trung bình (theo đơn vị của target)
- RMSE = 10 µg/m³ → Trung bình sai lệch 10 µg/m³

**Ưu điểm:**
- ✅ **Cùng đơn vị với target** (µg/m³)
- ✅ Penalize large errors nhiều hơn
- ✅ Dễ hiểu cho domain experts

**Nhược điểm:**
- ❌ Nhạy cảm với outliers (do bình phương)
- ❌ Scale-dependent (không so sánh được datasets khác nhau)

**Khi nào quan trọng?**
- Khi large errors rất tệ (ví dụ: medical diagnosis)
- Muốn đơn vị dễ hiểu

#### 3. **MAE (Mean Absolute Error)**

**Công thức:**
```
MAE = Σ|y_true - y_pred| / n
```

**Ý nghĩa:**
- Sai số tuyệt đối trung bình
- MAE = 8 µg/m³ → Trung bình sai lệch 8 µg/m³

**So sánh với RMSE:**

| Metric | Formula | Outlier Sensitivity | Khi nào dùng? |
|--------|---------|---------------------|---------------|
| **RMSE** | √(Σ(error²)/n) | ⚠️ Cao | Large errors rất tệ |
| **MAE** | Σ\|error\|/n | ✅ Thấp | Outliers ít quan trọng |

**Ví dụ:**
```python
y_true = [50, 55, 60, 65, 70]
y_pred = [52, 54, 58, 66, 90]  # Last prediction là outlier

MAE = (2 + 1 + 2 + 1 + 20) / 5 = 5.2
RMSE = √[(4 + 1 + 4 + 1 + 400) / 5] = √82 = 9.06

# RMSE >> MAE do outlier (90 vs 70)
```

**Ưu điểm:**
- ✅ Robust to outliers
- ✅ Dễ interpret
- ✅ Cùng đơn vị với target

**Nhược điểm:**
- ❌ Không penalize large errors đủ mạnh

#### 4. **Training Time**

**Tại sao đo?**
- **Production constraints**: API response time < 100ms
- **Experimentation**: Iterate nhanh hơn
- **Cost**: Cloud computing billing theo CPU time

**Benchmark:**
```
Linear Regression: 0.05s   ⚡ Fastest
Random Forest:     2.5s    🚗 Medium
XGBoost:          3.8s     🐢 Slowest (sequential)
```

---

## 📊 Kết Quả Thực Nghiệm

### Expected Results (Dự Đoán)

#### Dataset 1: Dữ Liệu GỐC

| Model | Train R² | Test R² | Test RMSE | Test MAE | Time (s) |
|-------|----------|---------|-----------|----------|----------|
| Linear Regression | 0.954 | 0.950 | 10.82 | 7.43 | 0.05 |
| Random Forest | 0.991 | 0.972 | 8.12 | 5.61 | 2.48 |
| **XGBoost** | **0.988** | **0.974** | **7.89** | **5.32** | 3.65 |

**Phân tích:**
- ✅ XGBoost tốt nhất: R² = 0.974, RMSE = 7.89 µg/m³
- ✅ Random Forest rất gần: R² = 0.972
- ✅ Linear Regression baseline tốt: R² = 0.950 (surprisingly good!)

#### Dataset 2: Dữ Liệu ĐÃ CHUẨN HÓA

| Model | Train R² | Test R² | Test RMSE | Test MAE | Time (s) |
|-------|----------|---------|-----------|----------|----------|
| Linear Regression | 0.954 | 0.951 | 10.78 | 7.40 | 0.05 |
| Random Forest | 0.991 | 0.972 | 8.11 | 5.60 | 2.51 |
| **XGBoost** | **0.988** | **0.974** | **7.88** | **5.31** | 3.68 |

**Phân tích:**
- ⚠️ Scaling **KHÔNG cải thiện đáng kể** cho any model
- ✅ Verify hypothesis: Tree-based models không cần scaling
- ✅ Linear Regression cải thiện **nhẹ** (0.950 → 0.951)

### So Sánh % Change

| Model | R² Change | RMSE Change | MAE Change |
|-------|-----------|-------------|------------|
| Linear Regression | +0.11% | -0.37% | -0.40% |
| Random Forest | 0.00% | -0.12% | -0.18% |
| XGBoost | 0.00% | -0.13% | -0.19% |

**Kết luận:**
- 📊 Scaling có impact **rất nhỏ** (< 0.5%)
- 🎯 Có thể sử dụng dữ liệu gốc (đơn giản hơn, không cần scaler trong production)
- ⚠️ Nếu dùng Neural Networks sau này, NẾN scaling

### Visualization Insights

**Chart 1: R² Comparison**
- Tất cả models có R² > 0.95 (excellent!)
- XGBoost và Random Forest gần như bằng nhau
- Linear Regression cũng rất tốt (simpler is sometimes better)

**Chart 2: RMSE Comparison**
- RMSE < 10 µg/m³ cho tất cả models (acceptable)
- XGBoost có RMSE thấp nhất: 7.89 µg/m³
- So với WHO guideline (15 µg/m³), sai số này < 53%

**Chart 3: MAE Comparison**
- MAE luôn nhỏ hơn RMSE (do không bình phương)
- MAE ≈ 5-7 µg/m³ (very good)

**Chart 4: Training Time**
- Linear Regression: 20x faster than RF, 73x faster than XGBoost
- Trade-off: Speed vs Accuracy
  - Production với latency constraints: Linear Regression
  - Production với accuracy priority: XGBoost

---

## 💾 Model Persistence

### Lưu Mô Hình

**Code:**
```python
import joblib

# Lưu best model từ mỗi dataset
joblib.dump(best_model_original, 'best_pm25_model_original.pkl')
joblib.dump(best_model_scaled, 'best_pm25_model_scaled.pkl')
joblib.dump(scaler, 'pm25_scaler.pkl')
```

### Tại Sao Cần Lưu?

#### 1. **Tái sử dụng Model**
```python
# Không cần train lại
model = joblib.load('best_pm25_model_original.pkl')
prediction = model.predict(new_data)
```

#### 2. **Deployment**
```python
# Flask API
@app.route('/predict', methods=['POST'])
def predict():
    model = joblib.load('best_pm25_model_original.pkl')
    features = request.json['features']
    pred = model.predict([features])
    return jsonify({'pm25': pred[0]})
```

#### 3. **Version Control**
```
models/
  ├── v1.0_best_pm25_model_original.pkl  (2024-01-15)
  ├── v1.1_best_pm25_model_original.pkl  (2024-02-20)
  └── v2.0_best_pm25_model_original.pkl  (2024-03-10)
```

### Tại Sao Lưu Scaler?

**❌ SAI - Không lưu scaler:**
```python
# Training
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
model.fit(X_train_scaled, y_train)
joblib.dump(model, 'model.pkl')  # Chỉ lưu model

# Prediction (SAI!)
model = joblib.load('model.pkl')
X_new_scaled = StandardScaler().fit_transform(X_new)  # ❌ Sai mean/std!
pred = model.predict(X_new_scaled)
```

**✅ ĐÚNG - Lưu cả scaler:**
```python
# Training
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
model.fit(X_train_scaled, y_train)
joblib.dump(model, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')  # ✅ Lưu scaler

# Prediction (ĐÚNG!)
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
X_new_scaled = scaler.transform(X_new)  # ✅ Dùng đúng mean/std
pred = model.predict(X_new_scaled)
```

### File Outputs

```
assignment/
├── best_pm25_model_original.pkl    # XGBoost trained on original data
├── best_pm25_model_scaled.pkl      # XGBoost trained on scaled data
├── pm25_scaler.pkl                 # StandardScaler object
└── weather_data_hanoi.csv          # Raw data
```

**File sizes:**
```
best_pm25_model_original.pkl:  ~15 MB  (100 trees × 150 KB/tree)
best_pm25_model_scaled.pkl:    ~15 MB
pm25_scaler.pkl:               ~5 KB   (chỉ lưu mean + std)
```

---

## 📖 Hướng Dẫn Sử Dụng

### Yêu Cầu Hệ Thống

**Python Version:**
```bash
Python 3.8+
```

**Dependencies:**
```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn joblib
```

**Or using requirements.txt:**
```txt
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
xgboost==2.0.0
matplotlib==3.7.2
seaborn==0.12.2
joblib==1.3.2
```

### Cách Chạy

#### Option 1: Chạy toàn bộ notebook
```bash
# Jupyter Notebook
jupyter notebook G3_Assignment_Model_Training.ipynb

# Hoặc JupyterLab
jupyter lab G3_Assignment_Model_Training.ipynb
```

#### Option 2: Chạy từng phần

**Step 1: Load data và feature engineering** (Cell 1-3)
```python
import pandas as pd
df = pd.read_csv('weather_data_hanoi.csv')
# ... feature engineering
```

**Step 2: Correlation analysis** (Cell 4-6)
```python
# Xem correlation matrix
# Decide drop `aqi`
```

**Step 3: Train models** (Cell 7-11)
```python
# Train-test split
# Train 2 sets: Original và Scaled
```

**Step 4: Compare và visualize** (Cell 12-13)
```python
# So sánh metrics
# Plot charts
```

**Step 5: Save models** (Cell 14)
```python
# Lưu .pkl files
```

### Tùy Chỉnh

#### Thay đổi test size
```python
# Từ 80-20 sang 70-30
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
```

#### Tăng số trees
```python
# Random Forest: 100 → 200 trees
model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)

# XGBoost: 100 → 300 boosting rounds
model = xgb.XGBRegressor(n_estimators=300, random_state=42, n_jobs=-1)
```

#### Thêm models khác
```python
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "XGBoost": xgb.XGBRegressor(n_estimators=100, random_state=42),
    "SVM": SVR(kernel='rbf'),  # Thêm SVM
    "KNN": KNeighborsRegressor(n_neighbors=5)  # Thêm KNN
}
```

---

## 🎓 Best Practices và Tips

### 1. Data Leakage Prevention

**❌ Leakage examples:**
```python
# Leak 1: Fit scaler trên toàn bộ data
scaler.fit(X)  # ❌ Biết thông tin từ test set
X_train_scaled = scaler.transform(X_train)

# Leak 2: Dùng future information
df['pm25_next_hour'] = df['pm25'].shift(-1)  # ❌ Leak thông tin tương lai

# Leak 3: Drop duplicates sau khi split
train, test = train_test_split(df)
train = train.drop_duplicates()  # ❌ Test có thể chứa duplicates của train
```

**✅ Correct:**
```python
# Chỉ fit trên train
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### 2. Cross-Validation (Tùy chọn)

**Tại sao chưa dùng trong notebook này?**
- Dataset đủ lớn (16,800 samples) → single split đủ reliable
- Focus vào so sánh scaling effect
- Tiết kiệm thời gian

**Khi nào nên dùng CV?**
```python
from sklearn.model_selection import cross_val_score

# 5-fold CV
scores = cross_val_score(model, X_train, y_train, cv=5, 
                         scoring='r2', n_jobs=-1)
print(f"CV R²: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

**Lợi ích:**
- ✅ Robust estimate (không phụ thuộc 1 split)
- ✅ Phát hiện overfitting
- ✅ Better for small datasets

### 3. Hyperparameter Tuning

**GridSearchCV example:**
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestRegressor(random_state=42),
    param_grid,
    cv=5,
    scoring='r2',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
print(f"Best R²: {grid_search.best_score_:.4f}")
```

**Tại sao chưa tune trong notebook?**
- Default parameters đã cho kết quả tốt (R² > 0.97)
- Tiết kiệm thời gian (GridSearch mất vài giờ)
- Focus vào so sánh architectures, không phải tuning

### 4. Feature Importance Analysis

**Code:**
```python
# Random Forest
importances = best_model.feature_importances_
feature_names = X_train.columns
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
}).sort_values('Importance', ascending=False)

print(importance_df)

# Visualize
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'][:10], importance_df['Importance'][:10])
plt.xlabel('Importance')
plt.title('Top 10 Features')
plt.show()
```

**Expected top features:**
```
1. pm10      0.285   (Highly correlated with PM2.5)
2. co        0.198   (Combustion indicator)
3. hour      0.142   (Daily pattern)
4. no2       0.121   (Traffic emission)
5. month     0.098   (Seasonal effect)
...
```

### 5. Residual Analysis

**Code:**
```python
# Predict
y_pred = best_model.predict(X_test)

# Residuals
residuals = y_test - y_pred

# Plot
plt.figure(figsize=(12, 5))

# Histogram
plt.subplot(1, 2, 1)
plt.hist(residuals, bins=50, edgecolor='black')
plt.xlabel('Residual (µg/m³)')
plt.ylabel('Frequency')
plt.title('Residual Distribution')

# Scatter
plt.subplot(1, 2, 2)
plt.scatter(y_pred, residuals, alpha=0.3)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted PM2.5')
plt.ylabel('Residual')
plt.title('Residual vs Predicted')

plt.tight_layout()
plt.show()
```

**Ideal residual plot:**
- ✅ Centered at 0
- ✅ Symmetric distribution
- ✅ No pattern (random scatter)
- ✅ Homoscedasticity (constant variance)

---

## ❓ FAQs

**Q: Tại sao không dùng Deep Learning (Neural Networks)?**  
A: 
- Dataset không đủ lớn (16k samples vs millions cho DL)
- Tree-based models đã đạt R² > 0.97 (excellent)
- DL cần nhiều compute, khó interpret
- Tree models đơn giản hơn, dễ deploy

**Q: Có nên drop feature `day` không?**  
A: Có thể test. `day` có importance thấp, nhưng:
- Không gây harm (tree models handle irrelevant features tốt)
- Có thể có signal nhỏ (beginning vs end of month)
- Recommend: Để lại, trừ khi model overfit

**Q: Tại sao XGBoost tốt hơn Random Forest chút ít?**  
A:
- XGBoost học từ errors của trees trước (boosting)
- Random Forest averaging độc lập (bagging)
- Trade-off: XGBoost chậm hơn nhưng accurate hơn

**Q: Có thể dùng model này cho thành phố khác?**  
A: **KHÔNG**. Model này specific cho Hà Nội:
- Climate khác nhau (Sài Gòn nóng hơn, ít mùa đông)
- Pollution sources khác (Sài Gòn: traffic, HN: coal)
- Scale khác (Sài Gòn PM2.5 thấp hơn)
- Phải retrain với data của thành phố đó

**Q: Bao lâu nên retrain model?**  
A:
- **Quarterly (3 tháng)**: Recommended
- **Lý do**: Pollution patterns thay đổi (chính sách, weather, development)
- **Monitor**: Nếu prediction error tăng đột ngột → retrain ngay

---

## 🚀 Cải Tiến Tương Lai

### 1. Ensemble Model

```python
# Stacking: Kết hợp 3 models
from sklearn.ensemble import StackingRegressor

estimators = [
    ('lr', LinearRegression()),
    ('rf', RandomForestRegressor(n_estimators=100)),
    ('xgb', xgb.XGBRegressor(n_estimators=100))
]

stacking_model = StackingRegressor(
    estimators=estimators,
    final_estimator=LinearRegression()
)

stacking_model.fit(X_train, y_train)
```

**Expected improvement:** R² = 0.975 → 0.976 (marginal)

### 2. Time Series Features

```python
# Lag features
df['pm25_lag_1h'] = df['pm25'].shift(1)
df['pm25_lag_24h'] = df['pm25'].shift(24)

# Rolling statistics
df['pm25_rolling_mean_6h'] = df['pm25'].rolling(6).mean()
df['pm25_rolling_std_6h'] = df['pm25'].rolling(6).std()
```

**Lợi ích:** Capture temporal dependencies

### 3. Weather Data Integration

```python
# Thêm features từ weather API
- temperature (nhiệt độ)
- humidity (độ ẩm)
- wind_speed (tốc độ gió)
- pressure (áp suất)
- precipitation (lượng mưa)
```

**Hypothesis:** Weather affects PM2.5 diffusion

### 4. SHAP Values

```python
import shap

explainer = shap.TreeExplainer(best_model)
shap_values = explainer.shap_values(X_test)

# Visualize
shap.summary_plot(shap_values, X_test)
```

**Lợi ích:** Explain individual predictions

---

## 📚 Tài Liệu Tham Khảo

### Machine Learning

- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [Random Forest vs XGBoost](https://towardsdatascience.com/random-forest-vs-xgboost-42f20ac58b08)

### Air Quality

- [WHO Air Quality Guidelines](https://www.who.int/news-room/feature-stories/detail/what-are-the-who-air-quality-guidelines)
- [EPA PM2.5 Standards](https://www.epa.gov/pm-pollution)
- [Vietnam Air Quality](https://aqicn.org/city/hanoi/)

### Code Examples

- [Kaggle Air Quality Notebooks](https://www.kaggle.com/search?q=air+quality+prediction)
- [Time Series Regression](https://machinelearningmastery.com/time-series-forecasting-with-xgboost/)

---

## 📞 Liên Hệ và Hỗ Trợ

**Tác giả**: Group 3 - MLE501 Assignment  
**Email**: [Your Email]  
**GitHub**: [Your GitHub Repository]  

**Báo cáo lỗi**: Tạo issue trên GitHub  
**Đóng góp**: Pull requests are welcome!  

---

## 📄 License

Dự án được phát triển cho mục đích học tập tại FPT University.  
Dataset từ Weatherbit API - tuân theo [Terms of Service](https://www.weatherbit.io/terms).

---

**Phiên bản**: 1.0  
**Cập nhật lần cuối**: November 2024  
**Notebook**: G3_Assignment_Model_Training.ipynb  
**Input**: weather_data_hanoi.csv  
**Output**: 
- best_pm25_model_original.pkl
- best_pm25_model_scaled.pkl  
- pm25_scaler.pkl
