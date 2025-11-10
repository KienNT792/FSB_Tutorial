# README - G3_Assignment_PM25_Prediction_7Days

## 📋 Mục Lục
1. [Tổng Quan](#tổng-quan)
2. [Mục Đích và Use Cases](#mục-đích-và-use-cases)
3. [Kiến Trúc Prediction Pipeline](#kiến-trúc-prediction-pipeline)
4. [Chi Tiết Kỹ Thuật](#chi-tiết-kỹ-thuật)
5. [Feature Generation](#feature-generation)
6. [Prediction Strategy](#prediction-strategy)
7. [So Sánh Hai Mô Hình](#so-sánh-hai-mô-hình)
8. [Visualization và Insights](#visualization-và-insights)
9. [Output và Export](#output-và-export)
10. [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)
11. [Limitations và Improvements](#limitations-và-improvements)

---

## 🎯 Tổng Quan

Notebook `G3_Assignment_PM25_Prediction_7Days.ipynb` là ứng dụng thực tế của các mô hình ML đã được huấn luyện để **dự báo nồng độ PM2.5 trong 7 ngày tiếp theo** (168 giờ). Đây là bước cuối cùng trong pipeline phân tích chất lượng không khí, biến mô hình từ experiment thành production tool.

### Workflow Tổng Thể

```
┌──────────────────────┐
│  Trained Models      │
│  - original.pkl      │
│  - scaled.pkl        │
│  - scaler.pkl        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Historical Data     │
│  weather_data_       │
│  hanoi.csv           │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Generate Future     │
│  Features            │
│  (168 hours)         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Predict with        │
│  2 Models            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Compare & Visualize │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Export Results      │
│  pm25_predictions_   │
│  comparison_7days.csv│
└──────────────────────┘
```

### Điểm Nổi Bật

- ✅ **7-day forecasting**: Dự báo 168 giờ (7 ngày × 24 giờ/ngày)
- ✅ **Dual model comparison**: So sánh Original vs Scaled models
- ✅ **Real-time applicable**: Có thể chạy hàng ngày để cập nhật dự báo
- ✅ **Comprehensive visualization**: 6 charts phân tích đa chiều
- ✅ **Air quality classification**: Đánh giá theo chuẩn EPA/WHO
- ✅ **Production-ready output**: CSV file với đầy đủ thông tin

---

## 🎪 Mục Đích và Use Cases

### Vấn Đề Thực Tế

**Scenario:**
```
Hôm nay: 10/11/2024
Câu hỏi: PM2.5 sẽ như thế nào trong 7 ngày tới (11-17/11)?
```

**Tại sao cần dự báo 7 ngày?**

1. **Cảnh báo sớm cho người dân**
   - Lên kế hoạch hoạt động ngoài trời
   - Chuẩn bị khẩu trang N95 khi cần
   - Tránh tập thể dục ngoài trời vào ngày xấu

2. **Ra quyết định chính sách**
   - Hạn chế giao thông trong ngày ô nhiễm cao
   - Đóng cửa nhà máy tạm thời
   - Phun nước làm sạch không khí

3. **Lập kế hoạch y tế**
   - Chuẩn bị thuốc ho, hô hấp
   - Tăng nhân lực bệnh viện
   - Khuyến cáo cho bệnh nhân hen suyễn

4. **Kinh doanh và sự kiện**
   - Quyết định tổ chức sự kiện outdoor
   - Lên lịch tour du lịch
   - Marketing máy lọc không khí

### Use Cases Cụ Thể

#### Use Case 1: Mobile App Alert
```
📱 Ứng Dụng "Hanoi Air Quality"

[Notification]
⚠️ Cảnh báo: PM2.5 sẽ ở mức UNHEALTHY 
   vào ngày 13/11 (Thứ 3)
   
   • Dự đoán: 78 µg/m³
   • Khuyến nghị: Hạn chế ra ngoài
   • Đeo khẩu trang N95 nếu cần thiết
```

#### Use Case 2: Government Dashboard
```
🏛️ Dashboard Chính Phủ

[7-Day Forecast]
━━━━━━━━━━━━━━━━━━━━━━━━━━
Mon: 45 µg/m³ ⚠️ Moderate
Tue: 68 µg/m³ 🔴 Unhealthy
Wed: 52 µg/m³ ⚠️ Moderate
Thu: 38 µg/m³ 🟡 Good
Fri: 42 µg/m³ ⚠️ Moderate
Sat: 35 µg/m³ 🟡 Good
Sun: 40 µg/m³ ⚠️ Moderate

[Action Needed]
• Thứ 3: Kích hoạt biện pháp hạn chế xe cộ
• Phun nước tại khu vực trung tâm
```

#### Use Case 3: Hospital Planning
```
🏥 Bệnh Viện Bạch Mai

[Dự Báo Bệnh Nhân Hô Hấp]
Dựa trên PM2.5 forecast:

Tuần tới:
• Ca khám dự kiến: +35% so với tuần trước
• Thuốc cần chuẩn bị: Ventolin, Seretide
• Nhân lực: Tăng 2 bác sĩ hô hấp ca chiều
```

---

## 🏗️ Kiến Trúc Prediction Pipeline

### Phase-by-Phase Architecture

```
┌────────────────────────────────────────────────────────┐
│                    PHASE 1: SETUP                      │
│  • Import libraries                                    │
│  • Configure warnings                                  │
│  • Display timestamp                                   │
└──────────────────────┬─────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────┐
│               PHASE 2: LOAD ARTIFACTS                  │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │ model_       │  │ model_       │  │ scaler.pkl  │  │
│  │ original.pkl │  │ scaled.pkl   │  │             │  │
│  └──────────────┘  └──────────────┘  └─────────────┘  │
└──────────────────────┬─────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────┐
│            PHASE 3: LOAD HISTORICAL DATA               │
│  • Load weather_data_hanoi.csv                         │
│  • Parse datetime                                      │
│  • Calculate feature statistics (mean)                 │
└──────────────────────┬─────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────┐
│          PHASE 4: GENERATE FUTURE TIMESTAMPS           │
│  • Find last date in historical data                   │
│  • Create 168 hourly timestamps (7 days)               │
│  • start_date + 1 day → end_date + 7 days              │
└──────────────────────┬─────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────┐
│           PHASE 5: FEATURE ENGINEERING                 │
│  Temporal Features:     Environmental Features:        │
│  • year                 • co (mean from history)       │
│  • month                • no2 (mean from history)      │
│  • day                  • o3 (mean from history)       │
│  • hour                 • pm10 (mean from history)     │
│  • weekday              • so2 (mean from history)      │
└──────────────────────┬─────────────────────────────────┘
                       │
                       ├────────────────────┬─────────────┐
                       │                    │             │
                       ▼                    ▼             ▼
           ┌──────────────────┐  ┌──────────────────┐   │
           │  PHASE 6a:       │  │  PHASE 6b:       │   │
           │  PREDICT         │  │  PREDICT         │   │
           │  with ORIGINAL   │  │  with SCALED     │   │
           │  - Direct input  │  │  - Scale first   │   │
           │  - model.predict │  │  - model.predict │   │
           └────────┬─────────┘  └────────┬─────────┘   │
                    │                     │              │
                    └──────────┬──────────┘              │
                               │                         │
                               ▼                         │
                   ┌──────────────────────┐              │
                   │  PHASE 7: COMPARE    │              │
                   │  • Calculate diff    │              │
                   │  • Compute % change  │              │
                   │  • Daily aggregation │              │
                   └──────────┬───────────┘              │
                              │                          │
                              ▼                          │
                   ┌──────────────────────┐              │
                   │  PHASE 8: VISUALIZE  │◄─────────────┘
                   │  • 6 charts          │
                   │  • Comparison plots  │
                   │  • Daily/hourly view │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  PHASE 9: EXPORT     │
                   │  • CSV generation    │
                   │  • Air quality class │
                   │  • Summary report    │
                   └──────────────────────┘
```

---

## 🔧 Chi Tiết Kỹ Thuật

### Phase 1: Setup và Import

**Code:**
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import joblib
import warnings
warnings.filterwarnings('ignore')
```

**Tại sao cần từng library?**

| Library | Purpose | Specific Use |
|---------|---------|--------------|
| **pandas** | Data manipulation | DataFrame cho predictions |
| **numpy** | Numerical operations | Array operations (nếu cần) |
| **matplotlib** | Plotting | 6 charts visualization |
| **seaborn** | Statistical plots | Heatmap, distribution |
| **datetime** | Time operations | Generate future timestamps |
| **joblib** | Model persistence | Load .pkl files |
| **warnings** | Suppress warnings | Clean output |

**warnings.filterwarnings('ignore'):**
```python
# Tại sao suppress warnings?
- Tránh clutter output với deprecation warnings
- Focus vào predictions results
- Production environment clean logs
```

### Phase 2: Load Trained Models

**Code:**
```python
model_original = joblib.load('best_pm25_model_original.pkl')
model_scaled = joblib.load('best_pm25_model_scaled.pkl')
scaler = joblib.load('pm25_scaler.pkl')
```

**Tại sao load cả 3 files?**

#### 1. **model_original.pkl**
```python
# Model trained on raw data
model_original = XGBRegressor(...)  # Đã được train
```

**Use case:**
- Dự báo trực tiếp từ raw features
- Không cần scaling step
- Faster prediction (1 step ít hơn)

#### 2. **model_scaled.pkl**
```python
# Model trained on scaled data
model_scaled = XGBRegressor(...)  # Đã được train trên scaled data
```

**Use case:**
- Dự báo từ scaled features
- Cần scaler.transform() trước
- So sánh với original

#### 3. **pm25_scaler.pkl**
```python
scaler = StandardScaler()
# mean_ = [340.5, 45.2, 52.1, ...]  # Đã fit từ training
# scale_ = [89.3, 15.4, 20.8, ...]
```

**Critical importance:**
```python
# ❌ SAI - Không có scaler
X_new_scaled = StandardScaler().fit_transform(X_new)  
# Sai mean/std → predictions hoàn toàn sai!

# ✅ ĐÚNG - Dùng scaler đã train
X_new_scaled = scaler.transform(X_new)
# Đúng mean/std → predictions chính xác
```

**Error handling:**
```python
try:
    model_original = joblib.load('best_pm25_model_original.pkl')
except Exception as e:
    print(f"Lỗi: {e}")
    model_original = None
```

**Tại sao try-except?**
- File không tồn tại → graceful fail
- Corrupted file → thông báo rõ ràng
- Missing models → hướng dẫn user fix

### Phase 3: Load Historical Data

**Code:**
```python
df = pd.read_csv('weather_data_hanoi.csv')
df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d:%H')
```

**Tại sao cần historical data?**

#### Use 1: Calculate Feature Means
```python
# Environmental features cho future predictions
co_mean = df['co'].mean()      # 365.7 µg/m³
no2_mean = df['no2'].mean()    # 48.3 µg/m³
o3_mean = df['o3'].mean()      # 55.1 µg/m³
pm10_mean = df['pm10'].mean()  # 82.4 µg/m³
so2_mean = df['so2'].mean()    # 28.6 µg/m³
```

**Rationale:**
- Không có dữ liệu thực tế cho tương lai
- Dùng historical mean là reasonable baseline
- Assumption: Environmental conditions stable

**Alternative approaches:**
```python
# Option 1: Last 7 days mean (more recent)
last_7_days = df[df['datetime'] >= df['datetime'].max() - timedelta(days=7)]
co_mean = last_7_days['co'].mean()

# Option 2: Seasonal mean (same month)
current_month = datetime.now().month
seasonal_data = df[df['month'] == current_month]
co_mean = seasonal_data['co'].mean()

# Option 3: ARIMA forecast (advanced)
# Forecast environmental features themselves
```

**Current choice: Overall mean**
- ✅ Simple, robust
- ✅ Không overly sensitive to recent outliers
- ⚠️ Assumption: Stable conditions

#### Use 2: Determine Last Date
```python
last_date = df['datetime'].max()  # 2024-11-09 23:00:00
start_date = last_date + timedelta(days=1)  # 2024-11-10 00:00:00
```

**Tại sao +1 day?**
- Dự báo cho **FUTURE**, không overlap với training data
- Tránh data leakage trong evaluation

---

## 🛠️ Feature Generation

### Phase 4: Generate Future Timestamps

**Code:**
```python
start_date = df['datetime'].max() + timedelta(days=1)
start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
end_date = start_date + timedelta(days=7)

future_dates = []
current = start_date
for i in range(168):  # 7 days × 24 hours
    future_dates.append(current)
    current += timedelta(hours=1)
```

**Tại sao 168 timestamps?**
```
7 days × 24 hours/day = 168 hours

Example:
2024-11-10 00:00
2024-11-10 01:00
2024-11-10 02:00
...
2024-11-16 22:00
2024-11-16 23:00
```

**Tại sao reset hour=0?**
```python
start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
```

**Lý do:**
- Bắt đầu từ **midnight** của ngày mới
- Consistent với training data (hourly granularity)
- Easier to interpret (full 7 days)

**Alternative: Start from current hour**
```python
# If current time is 14:30
start_date = datetime.now()  # 2024-11-10 14:30
# Forecast: 14:30 → 14:30 (7 days later)

# Pros: More immediate
# Cons: Partial days, harder to interpret
```

### Phase 5: Feature Engineering

**Code:**
```python
future_df = pd.DataFrame({
    'datetime': future_dates,
    'year': [d.year for d in future_dates],
    'month': [d.month for d in future_dates],
    'day': [d.day for d in future_dates],
    'hour': [d.hour for d in future_dates],
    'weekday': [d.weekday() for d in future_dates]
})

# Environmental features (use historical means)
for feature in ['co', 'no2', 'o3', 'pm10', 'so2']:
    future_df[feature] = df[feature].mean()
```

**Feature Overview:**

| Feature Type | Features | Values | Source |
|--------------|----------|--------|--------|
| **Temporal** | year, month, day, hour, weekday | Computed from datetime | Known (future dates) |
| **Environmental** | co, no2, o3, pm10, so2 | Historical mean | Estimated |

**Example DataFrame:**
```python
    datetime             year  month  day  hour  weekday  co      no2    o3     pm10   so2
0   2024-11-10 00:00:00  2024  11     10   0     6        365.7   48.3   55.1   82.4   28.6
1   2024-11-10 01:00:00  2024  11     10   1     6        365.7   48.3   55.1   82.4   28.6
2   2024-11-10 02:00:00  2024  11     10   2     6        365.7   48.3   55.1   82.4   28.6
...
167 2024-11-16 23:00:00  2024  11     16   23    5        365.7   48.3   55.1   82.4   28.6
```

**Key Insight:**
- **Temporal features VARY** (hour: 0→23, day: 10→16, weekday: 0→6)
- **Environmental features CONSTANT** (same mean for all 168 hours)

**Why this works?**
```
Model learned patterns like:
• PM2.5 high at hour=8 (rush hour) → Applies to future
• PM2.5 high in month=1 (winter) → Applies to future
• PM2.5 correlates with pm10 → Uses estimated pm10

Even with constant environmental features, 
temporal patterns drive predictions!
```

**Feature order matters?**
```python
feature_order = ['co', 'no2', 'o3', 'pm10', 'so2', 
                 'year', 'month', 'day', 'hour', 'weekday']
```

**Yes, must match training order:**
```python
# Training:
X_train columns: [co, no2, o3, pm10, so2, year, month, day, hour, weekday]

# Prediction (must match):
X_future columns: [co, no2, o3, pm10, so2, year, month, day, hour, weekday]

# ❌ Wrong order → Incorrect predictions
X_future columns: [year, month, co, no2, ...]  # Wrong!
```

---

## 🔮 Prediction Strategy

### Phase 6a: Predict với Original Model

**Code:**
```python
X_future = future_df.drop(columns=['datetime'])
predictions_original = model_original.predict(X_future)
future_df['pm25_predicted_original'] = predictions_original
```

**Flow:**
```
X_future (168 × 10)
    ↓
model_original.predict()
    ↓
predictions_original (168,)
    ↓
Add to DataFrame
```

**Tại sao drop datetime?**
```python
# DataFrame có datetime để tracking
# Nhưng model không train với datetime (đã extract thành year, month, etc.)
X_future = future_df.drop(columns=['datetime'])
```

**Statistics computed:**
```python
print(f"PM2.5 Mean: {predictions_original.mean():.2f} µg/m³")
print(f"PM2.5 Min: {predictions_original.min():.2f} µg/m³")
print(f"PM2.5 Max: {predictions_original.max():.2f} µg/m³")
print(f"PM2.5 Std: {predictions_original.std():.2f} µg/m³")
```

**Example output:**
```
PM2.5 Mean: 52.34 µg/m³
PM2.5 Min: 38.12 µg/m³
PM2.5 Max: 71.89 µg/m³
PM2.5 Std: 8.45 µg/m³
```

**Daily aggregation:**
```python
for day in range(7):
    day_start = start_date + timedelta(days=day)
    day_end = day_start + timedelta(days=1)
    day_mask = (future_df['datetime'] >= day_start) & (future_df['datetime'] < day_end)
    day_mean = future_df[day_mask]['pm25_predicted_original'].mean()
    print(f"Ngày {day+1}: Mean={day_mean:.2f}")
```

**Tại sao aggregate by day?**
- Easier to interpret (người dùng hiểu "ngày" hơn "168 giờ")
- Planning decisions thường theo ngày
- Smooth out hourly fluctuations

### Phase 6b: Predict với Scaled Model

**Code:**
```python
X_future = future_df.drop(columns=['datetime', 'pm25_predicted_original'])
X_future_scaled = scaler.transform(X_future)  # Scale first!
predictions_scaled = model_scaled.predict(X_future_scaled)
future_df['pm25_predicted_scaled'] = predictions_scaled
```

**Critical difference:**
```python
# Original model:
predictions = model_original.predict(X_future)  # Direct

# Scaled model:
X_future_scaled = scaler.transform(X_future)   # Scale first
predictions = model_scaled.predict(X_future_scaled)  # Then predict
```

**Scaling transformation:**
```python
# Before scaling
X_future[0] = [365.7, 48.3, 55.1, 82.4, 28.6, 2024, 11, 10, 0, 6]

# After scaling (example)
X_future_scaled[0] = [0.12, -0.34, 0.18, 0.45, -0.67, 1.23, 0.89, -0.12, -1.45, 0.78]
```

**Scaler parameters (learned from training):**
```python
scaler.mean_      # [365.7, 48.3, 55.1, ...]
scaler.scale_     # [89.3, 15.4, 20.8, ...]  (std)
```

**Why these specific values?**
- Computed from training data (X_train)
- **Must use same values** for consistency
- That's why we load scaler.pkl

---

## ⚖️ So Sánh Hai Mô Hình

### Phase 7: Comparison Analysis

**Code:**
```python
future_df['difference'] = abs(future_df['pm25_predicted_original'] - 
                               future_df['pm25_predicted_scaled'])
future_df['difference_percent'] = (future_df['difference'] / 
                                   future_df['pm25_predicted_original']) * 100
```

**Metrics computed:**

#### 1. **Absolute Difference**
```python
difference = |Original - Scaled|

Example:
Original: 52.3 µg/m³
Scaled:   50.8 µg/m³
Difference: 1.5 µg/m³
```

**Interpretation:**
- Small difference (< 5 µg/m³): Models agree
- Medium difference (5-10 µg/m³): Some disagreement
- Large difference (> 10 µg/m³): Significant disagreement

#### 2. **Percentage Difference**
```python
difference_percent = (|Original - Scaled| / Original) × 100

Example:
Difference: 1.5 µg/m³
Original: 52.3 µg/m³
Percentage: 2.87%
```

**Interpretation:**
- < 5%: Excellent agreement
- 5-10%: Good agreement
- > 10%: Poor agreement

### Comparison Statistics

**Overall comparison:**
```python
comparison_stats = pd.DataFrame({
    'Metric': ['Mean', 'Min', 'Max', 'Std'],
    'Original Model': [52.34, 38.12, 71.89, 8.45],
    'Scaled Model': [51.87, 37.56, 70.23, 8.12],
    'Difference': [0.47, 0.56, 1.66, 0.33]
})
```

**Daily comparison:**
```python
Ngày 1: Original=52.3, Scaled=51.8, Diff=0.5 µg/m³
Ngày 2: Original=54.2, Scaled=53.7, Diff=0.5 µg/m³
Ngày 3: Original=49.8, Scaled=49.1, Diff=0.7 µg/m³
...
```

### Tại Sao So Sánh?

#### Reason 1: **Model Validation**
```
If models disagree significantly:
→ One (or both) might be unreliable
→ Need to investigate why

If models agree:
→ Higher confidence in predictions
→ Models learned similar patterns
```

#### Reason 2: **Ensemble Opportunity**
```python
# Average of two models (simple ensemble)
future_df['pm25_average'] = (future_df['pm25_predicted_original'] + 
                              future_df['pm25_predicted_scaled']) / 2
```

**Benefits:**
- ✅ Reduce individual model bias
- ✅ Often more robust than single model
- ✅ Smooth out extreme predictions

#### Reason 3: **Production Decision**
```
Criteria for choosing model in production:

1. Consistency: Lower difference → Better
2. Historical performance: R², RMSE from training
3. Simplicity: Original model (no scaling step) → Faster
4. Use case: Real-time vs batch predictions

Decision:
- If difference < 5%: Use Original (simpler)
- If Scaled significantly better: Use Scaled (accept complexity)
- If uncertain: Use Average (ensemble)
```

---

## 📊 Visualization và Insights

### Phase 8: 6-Chart Comprehensive Analysis

**Overall figure:**
```python
fig, axes = plt.subplots(3, 2, figsize=(18, 16))
# 3 rows × 2 columns = 6 charts
```

#### Chart 1: Time Series Comparison (Top-Left)

**Code:**
```python
ax1.plot(future_df['datetime'], future_df['pm25_predicted_original'], 
         linewidth=2, color='#3498db', marker='o', label='Original')
ax1.plot(future_df['datetime'], future_df['pm25_predicted_scaled'], 
         linewidth=2, color='#e74c3c', marker='s', label='Scaled')
```

**Purpose:**
- Compare predictions side-by-side over time
- Identify when models disagree
- See overall trends

**Insights to look for:**
```
• Do models track each other closely?
• Are there specific time periods with large divergence?
• What's the general PM2.5 trend (increasing/decreasing)?
```

**Example pattern:**
```
PM2.5
 70 |              ╱╲              ╱╲
 60 |          ╱╲ ╱  ╲         ╱╲ ╱  ╲
 50 |     ╱╲ ╱  ╲╱    ╲    ╱╲ ╱  ╲╱    ╲
 40 |  ╱╲ ╱  ╲           ╱╲ ╱  ╲
    +────────────────────────────────
    Mon Tue Wed Thu Fri Sat Sun

Pattern: Rush hour peaks (8AM, 7PM)
```

#### Chart 2: Absolute Difference (Top-Right)

**Code:**
```python
ax2.fill_between(future_df['datetime'], future_df['difference'], 
                  alpha=0.5, color='orange')
ax2.axhline(y=future_df['difference'].mean(), color='red', 
            linestyle='--', label=f"Mean: {mean:.2f}")
```

**Purpose:**
- Visualize model agreement
- Identify periods of high uncertainty

**Interpretation:**
```
High difference peaks:
→ Models uncertain about these time periods
→ Consider taking average or adding safety margin

Consistently low difference:
→ High confidence in predictions
→ Models learned robust patterns
```

#### Chart 3: Daily Average - Original (Middle-Left)

**Code:**
```python
daily_means = []
for day in range(7):
    day_data = future_df[day_mask]['pm25_predicted_original'].mean()
    daily_means.append(day_data)

ax3.bar(range(7), daily_means, alpha=0.8, color='#3498db')
```

**Purpose:**
- Simplified daily view
- Planning decisions (which days are worse?)

**Example:**
```
Daily PM2.5 (Original Model)

 60 |     [56.2]           [58.1]
 50 |                             [49.3] [48.7]
 40 | [45.3]      [47.8]                        [44.2]
    +──────────────────────────────────────────────
    Mon   Tue   Wed   Thu   Fri   Sat   Sun

Insight: Thursday-Friday are best days for outdoor activities
```

#### Chart 4: Daily Average - Scaled (Middle-Right)

**Purpose:**
- Same as Chart 3 but for Scaled model
- Compare daily patterns between models

**Key comparison:**
```
If patterns similar:
→ Both models capture weekly cycle
→ Higher confidence

If patterns different:
→ Investigate why (training data issues?)
```

#### Chart 5: Hourly Pattern - Original (Bottom-Left)

**Code:**
```python
hourly_means = future_df.groupby('hour')['pm25_predicted_original'].mean()
ax5.plot(hourly_means.index, hourly_means.values, linewidth=3)
```

**Purpose:**
- Identify daily cycle
- Rush hour effects

**Expected pattern:**
```
PM2.5
 60 |     ╱╲              ╱╲
 55 |    ╱  ╲            ╱  ╲
 50 |   ╱    ╲__________╱    ╲
 45 |  ╱                      ╲___
    +──────────────────────────────
    0  4  8  12 16 20 24 (hour)
    
Peak times:
• 7-9 AM: Morning rush hour
• 6-8 PM: Evening rush hour

Low times:
• 2-5 AM: Minimal traffic
```

#### Chart 6: Hourly Pattern - Scaled (Bottom-Right)

**Purpose:**
- Compare hourly patterns
- Verify both models learned daily cycles

**Validation:**
```
Both models should show:
✅ Morning peak (7-9 AM)
✅ Evening peak (6-8 PM)
✅ Night valley (2-5 AM)

If one model doesn't:
⚠️ That model may have learned noise, not signal
```

### Visualization Best Practices

**Color scheme:**
```python
Original: Blue (#3498db)  - Cool, calm
Scaled:   Red (#e74c3c)   - Warm, attention
Difference: Orange        - Alert, caution
```

**Annotations:**
```python
# Add values on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}', ha='center', va='bottom')
```

**Grid lines:**
```python
ax.grid(True, alpha=0.3)  # Subtle, not distracting
```

---

## 📤 Output và Export

### Phase 9: CSV Generation

**Code:**
```python
result_df = future_df[['datetime', 'year', 'month', 'day', 'hour', 'weekday',
                       'pm25_predicted_original', 'pm25_predicted_scaled', 
                       'difference', 'difference_percent']].copy()

result_df.to_csv('pm25_predictions_comparison_7days.csv', 
                 index=False, encoding='utf-8-sig')
```

### CSV Structure

**Columns:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Datetime | datetime | Prediction timestamp | 2024-11-10 14:00:00 |
| Year | int | Year | 2024 |
| Month | int | Month (1-12) | 11 |
| Day | int | Day of month | 10 |
| Hour | int | Hour (0-23) | 14 |
| Weekday | int | Day of week (0=Mon) | 6 |
| Weekday_Name | str | Day name | Sunday |
| PM25_Original | float | Original model prediction | 52.34 |
| PM25_Scaled | float | Scaled model prediction | 51.87 |
| Difference | float | Absolute difference | 0.47 |
| Difference_Percent | float | Percentage difference | 0.90% |
| Air_Quality_Original | str | EPA classification | Unhealthy |
| Air_Quality_Scaled | str | EPA classification | Unhealthy |
| PM25_Average | float | Average of two models | 52.11 |
| Air_Quality_Average | str | EPA classification | Unhealthy |

**Total rows:** 168 (7 days × 24 hours)

### Air Quality Classification

**Function:**
```python
def get_air_quality(pm25):
    if pm25 <= 12:
        return 'Good'
    elif pm25 <= 35.4:
        return 'Moderate'
    elif pm25 <= 55.4:
        return 'Unhealthy for Sensitive Groups'
    elif pm25 <= 150.4:
        return 'Unhealthy'
    elif pm25 <= 250.4:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'
```

**Based on EPA AQI:**

| PM2.5 Range (µg/m³) | Category | Health Implications |
|---------------------|----------|---------------------|
| 0 - 12 | Good | No health impact |
| 12.1 - 35.4 | Moderate | Acceptable; some concern for very sensitive |
| 35.5 - 55.4 | Unhealthy for Sensitive | Sensitive groups experience effects |
| 55.5 - 150.4 | Unhealthy | Everyone experiences effects |
| 150.5 - 250.4 | Very Unhealthy | Health alert; everyone at risk |
| 250.5+ | Hazardous | Emergency conditions |

**Application:**
```python
result_df['Air_Quality_Original'] = result_df['PM25_Original'].apply(get_air_quality)
```

**Example distribution:**
```
Air Quality Distribution (168 hours):

Good:                              0 hours (0.0%)
Moderate:                         42 hours (25.0%)
Unhealthy for Sensitive Groups:   98 hours (58.3%)
Unhealthy:                        28 hours (16.7%)
Very Unhealthy:                    0 hours (0.0%)
Hazardous:                         0 hours (0.0%)
```

### Ensemble Prediction

**Code:**
```python
result_df['PM25_Average'] = (result_df['PM25_Original'] + 
                             result_df['PM25_Scaled']) / 2
```

**Tại sao ensemble?**

#### Benefit 1: Reduce Variance
```
Original: [50, 55, 60, 58, 52]
Scaled:   [52, 53, 58, 60, 54]
Average:  [51, 54, 59, 59, 53]  ← Smoother

Variance:
Original: 15.2
Scaled:   12.8
Average:  11.4  ← Lowest (most stable)
```

#### Benefit 2: Reduce Bias
```
If Original tends to overpredict:   +3 µg/m³
If Scaled tends to underpredict:    -2 µg/m³
Average bias:                        +0.5 µg/m³  ← Balanced
```

#### Benefit 3: Production Robustness
```
If one model fails:
- Still have other model
- Average gracefully degrades

If both models available:
- Ensemble typically more accurate
- Lower RMSE in practice
```

### CSV Usage Examples

#### Use Case 1: Load in Dashboard
```python
import pandas as pd

# Load predictions
pred_df = pd.read_csv('pm25_predictions_comparison_7days.csv')

# Filter bad air quality days
bad_days = pred_df[pred_df['Air_Quality_Average'] == 'Unhealthy']
print(f"⚠️ Warning: {len(bad_days)} hours of unhealthy air")

# Group by day
daily_summary = pred_df.groupby('Day')['PM25_Average'].agg(['mean', 'min', 'max'])
print(daily_summary)
```

#### Use Case 2: API Endpoint
```python
from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/api/forecast/<date>')
def get_forecast(date):
    df = pd.read_csv('pm25_predictions_comparison_7days.csv')
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    
    # Filter by date
    forecast = df[df['Datetime'].dt.date == pd.to_datetime(date).date()]
    
    return jsonify(forecast.to_dict(orient='records'))

# GET /api/forecast/2024-11-12
# Returns: [{datetime: ..., pm25: ..., air_quality: ...}, ...]
```

#### Use Case 3: Alert System
```python
def check_alerts(csv_file):
    df = pd.read_csv(csv_file)
    
    # Find dangerous periods
    alerts = []
    for idx, row in df.iterrows():
        if row['PM25_Average'] > 55.4:  # Unhealthy threshold
            alerts.append({
                'datetime': row['Datetime'],
                'pm25': row['PM25_Average'],
                'severity': row['Air_Quality_Average']
            })
    
    # Send notifications
    if alerts:
        send_email_alert(alerts)
        send_push_notification(alerts)
```

---

## 📖 Hướng Dẫn Sử Dụng

### Prerequisites

**Files required:**
```
assignment/
├── best_pm25_model_original.pkl   ✅ Required
├── best_pm25_model_scaled.pkl     ✅ Required
├── pm25_scaler.pkl                ✅ Required
├── weather_data_hanoi.csv         ✅ Required
└── G3_Assignment_PM25_Prediction_7Days.ipynb
```

**If missing:**
```bash
# Run training notebook first
jupyter notebook G3_Assignment_Model_Training.ipynb
# This will generate all .pkl files
```

**Python dependencies:**
```bash
pip install pandas numpy matplotlib seaborn joblib scikit-learn
```

### Running the Notebook

#### Step 1: Open notebook
```bash
jupyter notebook G3_Assignment_PM25_Prediction_7Days.ipynb
```

#### Step 2: Run all cells
```python
# Option A: Click "Run All" in menu
# Option B: Shift+Enter through each cell
```

#### Step 3: Check outputs

**Expected console output:**
```
======================================================================
LOAD MÔ HÌNH VÀ SCALER
======================================================================

✓ Đã load mô hình từ dữ liệu GỐC: best_pm25_model_original.pkl
   Loại mô hình: XGBRegressor
✓ Đã load mô hình từ dữ liệu ĐÃ CHUẨN HÓA: best_pm25_model_scaled.pkl
   Loại mô hình: XGBRegressor
✓ Đã load StandardScaler: pm25_scaler.pkl

======================================================================
...
```

#### Step 4: View visualizations

**6 charts should appear:**
1. Time series comparison
2. Difference plot
3-4. Daily averages (both models)
5-6. Hourly patterns (both models)

#### Step 5: Check CSV output

```bash
# File created
ls -lh pm25_predictions_comparison_7days.csv

# Preview
head pm25_predictions_comparison_7days.csv
```

### Automation Script

**Daily prediction script:**
```python
# daily_prediction.py
import subprocess
from datetime import datetime

def run_prediction():
    print(f"[{datetime.now()}] Starting PM2.5 prediction...")
    
    # Run notebook
    subprocess.run([
        'jupyter', 'nbconvert',
        '--to', 'notebook',
        '--execute',
        'G3_Assignment_PM25_Prediction_7Days.ipynb',
        '--output', f'predictions_{datetime.now().strftime("%Y%m%d")}.ipynb'
    ])
    
    print("✓ Prediction completed!")
    print("✓ Check pm25_predictions_comparison_7days.csv for results")

if __name__ == '__main__':
    run_prediction()
```

**Cron job (Linux/Mac):**
```bash
# Run daily at 6 AM
0 6 * * * cd /path/to/assignment && python daily_prediction.py
```

**Windows Task Scheduler:**
```
Action: Start a Program
Program: python
Arguments: C:\path\to\daily_prediction.py
Trigger: Daily at 6:00 AM
```

---

## ⚠️ Limitations và Improvements

### Current Limitations

#### 1. **Static Environmental Features**
```python
# Current approach
co_mean = df['co'].mean()  # Same for all 168 hours

# Limitation
- Real CO varies hour-by-hour, day-by-day
- Using constant mean ignores dynamic changes
```

**Impact:**
- Predictions rely heavily on temporal patterns
- May miss sudden environmental changes (e.g., factory shutdown, heavy rain)

**Improvement:**
```python
# Option 1: ARIMA forecast for environmental features
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(df['co'], order=(5,1,0))
model_fit = model.fit()
co_forecast = model_fit.forecast(steps=168)

# Option 2: Exponential smoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(df['co'], seasonal_periods=24)
model_fit = model.fit()
co_forecast = model_fit.forecast(168)

# Use forecasted values instead of mean
future_df['co'] = co_forecast
```

#### 2. **No Weather Data**
```python
# Missing features
- temperature (nhiệt độ)
- humidity (độ ẩm)
- wind_speed (tốc độ gió)
- precipitation (lượng mưa)
- pressure (áp suất)
```

**Why important?**
```
High wind speed → PM2.5 disperses → Lower pollution
High humidity → PM2.5 trapped → Higher pollution
Rain → Washes out particles → Lower pollution
```

**Improvement:**
```python
# Integrate weather forecast API
import requests

def get_weather_forecast(days=7):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': 'Hanoi',
        'appid': 'YOUR_API_KEY',
        'units': 'metric'
    }
    
    response = requests.get(url, params=params)
    weather_data = response.json()
    
    # Extract features
    temperatures = [item['main']['temp'] for item in weather_data['list']]
    humidity = [item['main']['humidity'] for item in weather_data['list']]
    wind_speed = [item['wind']['speed'] for item in weather_data['list']]
    
    return temperatures, humidity, wind_speed

# Add to future_df
temp, humid, wind = get_weather_forecast()
future_df['temperature'] = temp[:168]
future_df['humidity'] = humid[:168]
future_df['wind_speed'] = wind[:168]
```

#### 3. **No Uncertainty Quantification**
```python
# Current output
PM2.5 = 52.3 µg/m³  # Point estimate only

# Missing
- Confidence interval: [45.2, 59.4] µg/m³ (95% CI)
- Prediction interval: [38.1, 66.5] µg/m³ (95% PI)
```

**Improvement:**
```python
# Quantile Regression (get prediction intervals)
from sklearn.ensemble import GradientBoostingRegressor

# Train for different quantiles
model_lower = GradientBoostingRegressor(loss='quantile', alpha=0.05)
model_median = GradientBoostingRegressor(loss='quantile', alpha=0.50)
model_upper = GradientBoostingRegressor(loss='quantile', alpha=0.95)

# Predictions
lower_bound = model_lower.predict(X_future)
median = model_median.predict(X_future)
upper_bound = model_upper.predict(X_future)

# Visualization with confidence bands
plt.plot(datetime, median, label='Median')
plt.fill_between(datetime, lower_bound, upper_bound, 
                 alpha=0.3, label='90% Prediction Interval')
```

#### 4. **No Feedback Loop**
```python
# Current: One-way prediction
Historical Data → Train Model → Predict Future

# Missing: Learning from prediction errors
Actual PM2.5 (after 1 day) → Compare with prediction → Retrain
```

**Improvement:**
```python
# Daily update script
def update_model_with_actual():
    # Load yesterday's prediction
    pred_df = pd.read_csv('pm25_predictions_comparison_7days.csv')
    yesterday = datetime.now() - timedelta(days=1)
    
    # Get actual PM2.5 from API
    actual_pm25 = fetch_actual_pm25(yesterday)
    
    # Calculate error
    predicted_pm25 = pred_df[pred_df['Datetime'].dt.date == yesterday.date()]['PM25_Average'].mean()
    error = abs(actual_pm25 - predicted_pm25)
    
    # If error > threshold, retrain model
    if error > 10:  # 10 µg/m³ threshold
        print(f"⚠️ Large error detected: {error:.2f} µg/m³")
        print("Starting model retraining...")
        retrain_model()
```

#### 5. **Limited to 7 Days**
```python
# Current: Fixed 7-day horizon
future_dates = range(168)  # 7 days only

# Limitation
- Cannot forecast 14 days, 30 days
- Prediction quality degrades beyond 7 days
```

**Why 7 days?**
```
Trade-off:
• Short-term (1-3 days): High accuracy, limited planning window
• Medium-term (7 days): Good accuracy, practical planning
• Long-term (30 days): Low accuracy, very uncertain

7 days = Sweet spot for accuracy vs utility
```

**Improvement for longer horizons:**
```python
# Recursive forecasting (careful: error compounds)
def forecast_n_days(n_days=14):
    predictions = []
    
    for day in range(n_days):
        # Predict next day
        X_next = generate_features(day)
        pred = model.predict(X_next)
        predictions.append(pred)
        
        # Use prediction as input for next iteration
        # (if model uses lagged PM2.5)
    
    return predictions

# Or: Use specialized long-term forecasting models
# - LSTM (Long Short-Term Memory)
# - Prophet (Facebook's time series library)
```

### Future Improvements

#### 1. **Multi-Model Ensemble**
```python
# Current: 2 models (Original, Scaled)
# Future: N models with weights

models = {
    'xgboost': (model_xgb, 0.35),
    'random_forest': (model_rf, 0.30),
    'lightgbm': (model_lgb, 0.25),
    'catboost': (model_cat, 0.10)
}

# Weighted average
predictions = sum(model.predict(X) * weight 
                  for model, weight in models.values())
```

#### 2. **Real-Time Data Integration**
```python
# Fetch latest data from IoT sensors
def get_realtime_data():
    sensors = ['sensor_1', 'sensor_2', 'sensor_3']
    
    latest_data = []
    for sensor in sensors:
        data = fetch_from_sensor(sensor)
        latest_data.append(data)
    
    # Average across sensors
    return pd.DataFrame(latest_data).mean()

# Use for prediction instead of historical mean
```

#### 3. **Spatial Predictions**
```python
# Current: Single point (Hanoi average)
# Future: Map-based predictions (different districts)

districts = ['Hoan Kiem', 'Ba Dinh', 'Cau Giay', 'Dong Da']

predictions_by_district = {}
for district in districts:
    model = load_model(f'model_{district}.pkl')
    pred = model.predict(X_future)
    predictions_by_district[district] = pred

# Heatmap visualization
plot_heatmap(predictions_by_district)
```

#### 4. **Mobile App Integration**
```python
# REST API for mobile apps
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/forecast/current', methods=['GET'])
def get_current_forecast():
    """Get next 24 hours forecast"""
    df = pd.read_csv('pm25_predictions_comparison_7days.csv')
    next_24h = df.head(24)
    return jsonify(next_24h.to_dict(orient='records'))

@app.route('/api/forecast/week', methods=['GET'])
def get_week_forecast():
    """Get full 7-day forecast"""
    df = pd.read_csv('pm25_predictions_comparison_7days.csv')
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/alert/check', methods=['GET'])
def check_alert():
    """Check if any alerts for next 24h"""
    df = pd.read_csv('pm25_predictions_comparison_7days.csv')
    next_24h = df.head(24)
    
    alerts = []
    for _, row in next_24h.iterrows():
        if row['PM25_Average'] > 55.4:
            alerts.append({
                'time': row['Datetime'],
                'pm25': row['PM25_Average'],
                'severity': row['Air_Quality_Average']
            })
    
    return jsonify({'has_alert': len(alerts) > 0, 'alerts': alerts})
```

---

## 📚 Tài Liệu Tham Khảo

### Air Quality Standards
- [EPA AQI Technical Assistance](https://www.airnow.gov/aqi/)
- [WHO Air Quality Guidelines 2021](https://www.who.int/publications/i/item/9789240034228)
- [Vietnam Air Quality Monitoring](https://aqicn.org/city/hanoi/)

### Forecasting Methods
- [Time Series Forecasting Guide](https://otexts.com/fpp3/)
- [Ensemble Methods](https://scikit-learn.org/stable/modules/ensemble.html)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)

### Similar Projects
- [Beijing PM2.5 Prediction (Kaggle)](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india)
- [Air Quality Forecasting with ML](https://www.mdpi.com/2073-4433/11/6/590)

---

## ❓ FAQs

**Q: Tại sao không dự báo 30 ngày hoặc dài hơn?**  
A: 
- Prediction error compounds over time
- Beyond 7 days, uncertainty quá lớn
- Environmental conditions change unpredictably
- 7 ngày là balance giữa accuracy và utility

**Q: Làm sao biết predictions có chính xác không?**  
A:
- Wait for actual data (sau 1 ngày)
- Compare với actual PM2.5 from monitoring stations
- Calculate RMSE, MAE on realized values
- Retrain nếu error cao

**Q: Có thể dùng cho thành phố khác không?**  
A: **KHÔNG trực tiếp**. Cần:
- Thu thập data của thành phố đó (weather_data_X.csv)
- Retrain models với data mới
- Validate performance
- Deploy riêng cho thành phố đó

**Q: Tại sao hai models predict khác nhau?**  
A:
- Training trên data khác nhau (scaled vs unscaled)
- Random initialization trong XGBoost
- Small numerical differences compound
- Difference < 5% là acceptable

**Q: Predictions có reliable trong điều kiện bất thường không (vd: cháy rừng)?**  
A: **KHÔNG**. Model trained trên normal conditions:
- Không có data về sự kiện extreme
- Predictions sẽ underestimate trong extreme events
- Cần manual override hoặc real-time correction

**Q: Làm sao deploy vào production?**  
A:
1. Wrap trong REST API (Flask/FastAPI)
2. Schedule daily runs (cron job)
3. Store predictions trong database
4. Frontend/mobile app consume API
5. Monitor prediction accuracy
6. Retrain model định kỳ (monthly)

---

## 📞 Liên Hệ và Hỗ Trợ

**Tác giả**: Group 3 - MLE501 Assignment  
**Email**: [Your Email]  
**GitHub**: [Your Repository]  

**Báo cáo lỗi**: Create issue trên GitHub  
**Đóng góp**: Pull requests welcome!  

**Support channels:**
- 📧 Email: For detailed questions
- 💬 GitHub Issues: For bugs and features
- 📖 Documentation: Check README first

---

## 📄 License

Dự án được phát triển cho mục đích học tập tại FPT University.  
Data từ Weatherbit API - tuân theo [Terms of Service](https://www.weatherbit.io/terms).

---

**Phiên bản**: 1.0  
**Cập nhật lần cuối**: November 2024  
**Notebook**: G3_Assignment_PM25_Prediction_7Days.ipynb  
**Input**: 
- best_pm25_model_original.pkl
- best_pm25_model_scaled.pkl
- pm25_scaler.pkl
- weather_data_hanoi.csv

**Output**: 
- pm25_predictions_comparison_7days.csv
- 6 visualization charts
- Console summary report
