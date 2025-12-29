# 📋 PIPELINE DỰ ÁN DỰ ĐOÁN PM2.5 HÀ NỘI

## 🎯 Tổng quan Pipeline

Pipeline hoàn chỉnh từ thu thập dữ liệu đến deployment cho bài toán dự đoán nồng độ PM2.5 tại Hà Nội.

---

## 🔄 PIPELINE WORKFLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                     1. DATA COLLECTION                          │
│  ┌─────────────────┐        ┌──────────────────┐              │
│  │ Weather API     │───────▶│ Weather CSV      │              │
│  │ (Weatherbit)    │        │ 24,025 records   │              │
│  └─────────────────┘        └──────────────────┘              │
│                                                                  │
│  ┌─────────────────┐        ┌──────────────────┐              │
│  │ Air Quality API │───────▶│ Air Quality CSV  │              │
│  │ (Weatherbit)    │        │ 24,059 records   │              │
│  └─────────────────┘        └──────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                     2. DATA INTEGRATION                         │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ • Merge on datetime (inner join)                     │      │
│  │ • Convert datetime format: YYYY-MM-DD:HH             │      │
│  │ • Sort by timestamp                                  │      │
│  │ • Result: ~24,000 merged hourly records              │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                     3. DATA CLEANING                            │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ Missing Values Handling:                             │      │
│  │ • Forward fill (time series)                         │      │
│  │ • Linear interpolation for gradual changes           │      │
│  │                                                       │      │
│  │ Outlier Treatment:                                   │      │
│  │ • Clipping at 1% and 99% quantiles                   │      │
│  │ • Keep PM2.5 outliers (real pollution events)        │      │
│  │                                                       │      │
│  │ Data Leak Removal:                                   │      │
│  │ • Drop AQI (calculated from PM2.5)                   │      │
│  │ • Drop app_temp (high correlation with temp)         │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                  4. FEATURE ENGINEERING                         │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ A. Time Features:                                    │      │
│  │    • hour, day_of_week, month, year                  │      │
│  │    • is_rush_hour (7-9h, 17-19h)                     │      │
│  │    • is_weekend                                      │      │
│  │                                                       │      │
│  │ B. Cyclical Encoding:                                │      │
│  │    • wind_dir → wind_dir_sin, wind_dir_cos           │      │
│  │    • hour → hour_sin, hour_cos                       │      │
│  │                                                       │      │
│  │ C. Lag Features (Time Series):                       │      │
│  │    • pm25_lag1, pm25_lag3, pm25_lag6                 │      │
│  │    • temp_lag1, wind_spd_lag1                        │      │
│  │                                                       │      │
│  │ D. Rolling Statistics:                               │      │
│  │    • pm25_ma3, pm25_ma6 (moving average)             │      │
│  │    • temp_ma3, wind_spd_ma3                          │      │
│  │                                                       │      │
│  │ E. Interaction Features:                             │      │
│  │    • wind_temp = wind_spd × temp                     │      │
│  │    • rh_temp = rh × temp                             │      │
│  │    • wind_rh = wind_spd × rh                         │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                   5. DATA NORMALIZATION                         │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ StandardScaler:                                      │      │
│  │ • Apply to all features (NOT target pm25)            │      │
│  │ • Save scaler for deployment                         │      │
│  │ • Transform: (X - mean) / std                        │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                   6. TRAIN-TEST SPLIT                           │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ Time-based Split (NO SHUFFLE):                       │      │
│  │ • Train: 70% (earliest data)                         │      │
│  │ • Validation: 15% (middle data)                      │      │
│  │ • Test: 15% (latest data)                            │      │
│  │                                                       │      │
│  │ ⚠️ CRITICAL: Preserve time order to prevent leakage │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                   7. MODEL TRAINING                             │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ Baseline Models:                                     │      │
│  │ ✓ Linear Regression (R² ~0.75)                       │      │
│  │ ✓ Ridge Regression (R² ~0.80)                        │      │
│  │                                                       │      │
│  │ Tree-based Models:                                   │      │
│  │ ✓ Random Forest (R² ~0.85-0.90)                      │      │
│  │ ✓ XGBoost (R² ~0.88-0.92) ⭐ RECOMMENDED            │      │
│  │ ✓ LightGBM (R² ~0.87-0.91)                           │      │
│  │                                                       │      │
│  │ Advanced Models:                                     │      │
│  │ ✓ Neural Network (R² ~0.82-0.90)                     │      │
│  │ ✓ LSTM (Time series, optional)                       │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│               8. HYPERPARAMETER TUNING                          │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ XGBoost Parameters:                                  │      │
│  │ • n_estimators: 100-500                              │      │
│  │ • max_depth: 3-8                                     │      │
│  │ • learning_rate: 0.01-0.1                            │      │
│  │ • subsample: 0.7-1.0                                 │      │
│  │ • colsample_bytree: 0.7-1.0                          │      │
│  │                                                       │      │
│  │ Method: TimeSeriesSplit Cross-Validation             │      │
│  │ Search: GridSearchCV or RandomizedSearchCV           │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                    9. MODEL EVALUATION                          │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ Metrics:                                             │      │
│  │ • RMSE: Root Mean Squared Error (target: <15)       │      │
│  │ • MAE: Mean Absolute Error (target: <10)            │      │
│  │ • R² Score: Explained variance (target: >0.85)      │      │
│  │ • MAPE: Mean Absolute % Error (target: <20%)        │      │
│  │                                                       │      │
│  │ Validation:                                          │      │
│  │ • Test set evaluation                                │      │
│  │ • Residual analysis                                  │      │
│  │ • Feature importance analysis                        │      │
│  │ • Error distribution check                           │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────┐
│                   10. MODEL DEPLOYMENT                          │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ • Save best model (pickle/joblib)                    │      │
│  │ • Save scaler object                                 │      │
│  │ • Create prediction API/function                     │      │
│  │ • Build monitoring dashboard                         │      │
│  │ • Setup alert system                                 │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 CHI TIẾT PIPELINE THEO GIAI ĐOẠN

### **GIAI ĐOẠN 1: DATA COLLECTION**

**Nguồn dữ liệu:**
- API: Weatherbit.io
- Tần suất: Hourly data
- Thời gian: 2023-2025 (khoảng 24,000 records)

**Output:**
- `hanoi_weather_history.csv`: 12 features
- `hanoi_air_quality_history.csv`: 8 features

---

### **GIAI ĐOẠN 2: DATA INTEGRATION**

```python
# Merge strategy
merged_df = pd.merge(
    df_weather, 
    df_air, 
    on='datetime', 
    how='inner'  # Only keep matching timestamps
)
```

**Key Actions:**
1. Convert datetime: `YYYY-MM-DD:HH` → datetime object
2. Sort by timestamp
3. Verify data alignment

---

### **GIAI ĐOẠN 3: DATA CLEANING**

#### **3.1 Missing Values**
```python
# Time series specific handling
merged_df = merged_df.fillna(method='ffill')  # Forward fill
# OR
merged_df = merged_df.interpolate(method='linear')  # Linear interpolation
```

#### **3.2 Outliers**
```python
# Clip outliers but keep PM2.5 extremes
for col in numeric_features:
    if col != 'pm25':
        Q1 = merged_df[col].quantile(0.01)
        Q99 = merged_df[col].quantile(0.99)
        merged_df[col] = merged_df[col].clip(lower=Q1, upper=Q99)
```

#### **3.3 Data Leak Prevention**
```python
# Remove features that leak information
merged_df = merged_df.drop(columns=['aqi', 'app_temp'])
```

---

### **GIAI ĐOẠN 4: FEATURE ENGINEERING**

#### **4.1 Time Features**
```python
merged_df['hour'] = merged_df['datetime'].dt.hour
merged_df['day_of_week'] = merged_df['datetime'].dt.dayofweek
merged_df['month'] = merged_df['datetime'].dt.month
merged_df['is_rush_hour'] = merged_df['hour'].isin([7,8,9,17,18,19]).astype(int)
merged_df['is_weekend'] = merged_df['day_of_week'].isin([5,6]).astype(int)
```

#### **4.2 Cyclical Encoding**
```python
# Wind direction (0° = 360°)
merged_df['wind_dir_sin'] = np.sin(np.deg2rad(merged_df['wind_dir']))
merged_df['wind_dir_cos'] = np.cos(np.deg2rad(merged_df['wind_dir']))

# Hour of day
merged_df['hour_sin'] = np.sin(2 * np.pi * merged_df['hour'] / 24)
merged_df['hour_cos'] = np.cos(2 * np.pi * merged_df['hour'] / 24)
```

#### **4.3 Lag Features**
```python
# PM2.5 lag features
merged_df['pm25_lag1'] = merged_df['pm25'].shift(1)
merged_df['pm25_lag3'] = merged_df['pm25'].shift(3)
merged_df['pm25_lag6'] = merged_df['pm25'].shift(6)

# Weather lag features
merged_df['temp_lag1'] = merged_df['temp'].shift(1)
merged_df['wind_spd_lag1'] = merged_df['wind_spd'].shift(1)
```

#### **4.4 Rolling Statistics**
```python
# Moving averages
merged_df['pm25_ma3'] = merged_df['pm25'].rolling(window=3).mean()
merged_df['pm25_ma6'] = merged_df['pm25'].rolling(window=6).mean()
merged_df['temp_ma3'] = merged_df['temp'].rolling(window=3).mean()
```

#### **4.5 Interaction Features**
```python
merged_df['wind_temp'] = merged_df['wind_spd'] * merged_df['temp']
merged_df['rh_temp'] = merged_df['rh'] * merged_df['temp']
merged_df['wind_rh'] = merged_df['wind_spd'] * merged_df['rh']
```

---

### **GIAI ĐOẠN 5: NORMALIZATION**

```python
from sklearn.preprocessing import StandardScaler

# Separate features and target
X = merged_df.drop(columns=['pm25', 'datetime'])
y = merged_df['pm25']

# Standardize features ONLY
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# IMPORTANT: Save scaler for deployment
import joblib
joblib.dump(scaler, 'scaler.pkl')
```

---

### **GIAI ĐOẠN 6: TRAIN-TEST SPLIT**

```python
# Time-based split (NO SHUFFLE!)
train_size = int(len(X_scaled) * 0.70)
val_size = int(len(X_scaled) * 0.15)

X_train = X_scaled[:train_size]
y_train = y[:train_size]

X_val = X_scaled[train_size:train_size+val_size]
y_val = y[train_size:train_size+val_size]

X_test = X_scaled[train_size+val_size:]
y_test = y[train_size+val_size:]
```

---

### **GIAI ĐOẠN 7: MODEL TRAINING**

#### **XGBoost (Recommended)**
```python
import xgboost as xgb

model = xgb.XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=50,
    verbose=100
)
```

#### **Random Forest**
```python
from sklearn.ensemble import RandomForestRegressor

rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)
```

---

### **GIAI ĐOẠN 8: HYPERPARAMETER TUNING**

```python
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV

# Time series cross-validation
tscv = TimeSeriesSplit(n_splits=5)

# Parameter grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [4, 6, 8],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.8, 0.9, 1.0]
}

grid_search = GridSearchCV(
    xgb.XGBRegressor(),
    param_grid,
    cv=tscv,
    scoring='neg_mean_squared_error',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
```

---

### **GIAI ĐOẠN 9: MODEL EVALUATION**

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

# Predictions
y_pred = model.predict(X_test)

# Calculate metrics
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

print(f"RMSE: {rmse:.2f} μg/m³")
print(f"MAE: {mae:.2f} μg/m³")
print(f"R² Score: {r2:.4f}")
print(f"MAPE: {mape:.2f}%")

# Feature importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 Features:")
print(importance.head(10))
```

---

### **GIAI ĐOẠN 10: DEPLOYMENT**

```python
# Save model
joblib.dump(model, 'pm25_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Prediction function
def predict_pm25(weather_data):
    """
    Predict PM2.5 from weather data
    
    Parameters:
    -----------
    weather_data : dict
        Dictionary containing weather features
        
    Returns:
    --------
    prediction : float
        Predicted PM2.5 value
    """
    # Load model and scaler
    model = joblib.load('pm25_model.pkl')
    scaler = joblib.load('scaler.pkl')
    
    # Prepare features
    features = prepare_features(weather_data)
    
    # Scale
    features_scaled = scaler.transform(features)
    
    # Predict
    prediction = model.predict(features_scaled)[0]
    
    return prediction
```

---

## 🎯 PERFORMANCE TARGETS

| Metric | Minimum | Target | Excellent |
|--------|---------|--------|-----------|
| **R² Score** | ≥ 0.80 | ≥ 0.85 | ≥ 0.90 |
| **RMSE** | ≤ 20 μg/m³ | ≤ 15 μg/m³ | ≤ 12 μg/m³ |
| **MAE** | ≤ 15 μg/m³ | ≤ 10 μg/m³ | ≤ 8 μg/m³ |
| **MAPE** | ≤ 25% | ≤ 20% | ≤ 15% |

---

## 🚨 CRITICAL BEST PRACTICES

### ✅ DO:
- ✅ Convert datetime before merging
- ✅ Remove data leakage features (AQI, app_temp)
- ✅ Use cyclical encoding for wind direction
- ✅ Create lag and rolling features for time series
- ✅ Use forward fill for missing values
- ✅ Keep PM2.5 outliers (real events)
- ✅ Scale features but NOT target
- ✅ Use time-based train-test split
- ✅ Save scaler for deployment

### ❌ DON'T:
- ❌ Don't use AQI as a feature
- ❌ Don't remove PM2.5 outliers
- ❌ Don't shuffle time series data
- ❌ Don't use mean/median imputation for time series
- ❌ Don't forget to save the scaler
- ❌ Don't normalize before splitting (causes leakage)
- ❌ Don't use KFold for time series (use TimeSeriesSplit)

---

## 📈 EXPECTED RESULTS

### **Model Comparison**

| Model | R² | RMSE | MAE | Training Time | Recommendation |
|-------|-----|------|-----|--------------|----------------|
| Linear Regression | 0.75 | 20 | 15 | Fast | Baseline |
| Ridge Regression | 0.80 | 18 | 13 | Fast | Baseline |
| Random Forest | 0.87 | 14 | 10 | Medium | ✓ Good |
| **XGBoost** | **0.90** | **12** | **8** | Medium | **✓✓ Best** |
| LightGBM | 0.89 | 13 | 9 | Fast | ✓ Good |
| Neural Network | 0.85 | 15 | 11 | Slow | Optional |

---

## 🔧 TOOLS & LIBRARIES

- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **ML Models**: scikit-learn, xgboost, lightgbm
- **Evaluation**: sklearn.metrics
- **Deployment**: joblib, pickle

---

## 📝 CHECKLIST

- [ ] Data collection completed
- [ ] Data merged and cleaned
- [ ] Missing values handled
- [ ] Outliers processed
- [ ] Features engineered (time, lag, rolling, interaction)
- [ ] Cyclical encoding applied
- [ ] Data normalized (features only)
- [ ] Train-test split (time-based)
- [ ] Baseline models trained
- [ ] XGBoost trained and tuned
- [ ] Model evaluated on test set
- [ ] Feature importance analyzed
- [ ] Model and scaler saved
- [ ] Prediction function created
- [ ] Documentation completed

---

**Dự án**: DAM501 - Dự đoán PM2.5 Hà Nội  
**Ngày**: Tháng 12, 2025  
**Phương pháp**: CRISP-DM
