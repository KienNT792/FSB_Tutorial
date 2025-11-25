# 📋 **PLAN: XÂY DỰNG MÔ HÌNH DỰ ĐOÁN PM2.5 HÀ NỘI**

## **BƯỚC 1: DATA COLLECTION & IMPORT** 

### 1.1 Thu thập dữ liệu
- [x] **Weather data:** `hanoi_weather_history.csv` - Dữ liệu thời tiết Hà Nội
- [x] **Air quality data:** `hanoi_air_quality_history.csv` - Dữ liệu chất lượng không khí Hà Nội
- [x] **Timeframe:** 2022-2025 (khoảng 3 năm dữ liệu)

### 1.2 Import libraries
- [x] **Data processing:** `pandas`, `numpy`
- [x] **Visualization:** `matplotlib`, `seaborn` 
- [x] **Machine Learning:** `sklearn`, `xgboost`
- [x] **Metrics:** `mean_squared_error`, `r2_score`, `mean_absolute_error`

### 1.3 Load datasets
- [x] Load `df_weather` từ weather CSV file
- [x] Load `df_air` từ air quality CSV file  
- [x] **Initial inspection:** `.info()`, `.head()`, `.shape`

---

## **BƯỚC 2: DATA UNDERSTANDING & INTEGRATION** 

### 2.1 Data Understanding
- [x] **Weather features analysis:** 12 cột 
  - `datetime`, `temp`, `app_temp`, `rh`, `wind_spd`, `wind_dir`
  - `pres`, `vis`, `clouds`, `precip`, `uv`, `dewpt`
- [x] **Air quality features analysis:** 8 cột
  - `datetime`, `aqi`, `pm25` (TARGET), `pm10`, `o3`, `so2`, `no2`, `co`

### 2.2 Data Quality Check
- [x] **Datetime format:** `YYYY-MM-DD:HH` (e.g., `2022-12-31:17`)
- [x] **Records count:** Weather (~24,024), Air quality (~24,058)
- [x] **Time range:** 2022-12-31 đến 2025-10-30
- [x] **Data types:** Mixed (object, float64, int64)

### 2.3 Data Integration
- [x] **Datetime conversion:** String → datetime format
- [x] **Data merge:** Inner join on datetime column  
- [x] **Merged dataset:** Combined weather + air quality data
- [x] **Quality check:** Verify merged data integrity

---

## **BƯỚC 3: EXPLORATORY DATA ANALYSIS (EDA)** 

### 3.1 Phân tích dữ liệu cơ bản
- [ ] Kiểm tra **missing values** và outliers trong merged_df
- [ ] Thống kê mô tả cho tất cả các features
- [ ] Phân bố của target variable (pm25)
- [ ] **Data quality assessment** và data cleaning needs

### 3.2 Phân tích tương quan
- [ ] **Correlation matrix** giữa các weather features và pm25
- [ ] **Heatmap visualization** cho correlation
- [ ] **Feature importance ranking** - top predictors
- [ ] **Multicollinearity check** - VIF analysis

### 3.3 Time Series Analysis  
- [ ] **Xu hướng PM2.5 theo thời gian** (ngày, tháng, năm)
- [ ] **Seasonality analysis** - pattern theo mùa (đông/hè)
- [ ] **Daily/Weekly patterns** - pattern theo giờ và ngày trong tuần
- [ ] **Trend decomposition** - trend, seasonal, residual

### 3.4 Weather Impact Analysis
- [ ] PM2.5 vs **Wind Speed** (scatter plot + regression line)
- [ ] PM2.5 vs **Humidity & Temperature** 
- [ ] PM2.5 vs **Precipitation** (rainy vs dry days analysis)
- [ ] **Atmospheric pressure** vs PM2.5 relationship
- [ ] **Air quality categorization** theo WHO standards

---
## **BƯỚC 4: DATA PREPROCESSING** 

### 4.1 Feature Engineering
- [ ] **Time-based features:**
  - `hour`, `day_of_week`, `month`, `season`, `year`
  - `is_weekend`, `is_rush_hour`, `is_holiday`
- [ ] **Weather interaction features:**
  - `temp_humidity_ratio`, `wind_pressure_index`
  - `atmospheric_stability` (based on temp gradients)
- [ ] **Lag features:** PM2.5, wind_spd từ 1h, 3h, 6h, 12h trước
- [ ] **Rolling statistics:** Moving averages (3h, 6h, 24h)

### 4.2 Data Cleaning
- [ ] **Outlier detection & treatment:** IQR method hoặc Z-score  
- [ ] **Missing value imputation:** Time-series interpolation
- [ ] **Feature selection:** Based on correlation + domain knowledge
- [ ] **Data validation:** Ensure logical ranges cho tất cả features

### 4.3 Data Transformation
- [ ] **Normalization/Standardization:** MinMaxScaler hoặc StandardScaler
- [ ] **Categorical encoding:** If any categorical variables exist
- [ ] **Target transformation:** Log transform if needed for PM2.5
- [ ] **Train-Validation-Test split:** 70-15-15 hoặc temporal split

---

## **BƯỚC 5: MODEL DEVELOPMENT** 

### 5.1 Baseline Models
- [ ] **Linear Regression** - simple baseline
- [ ] **Random Forest Regressor** - tree-based ensemble  
- [ ] **XGBoost Regressor** - gradient boosting
- [ ] **Support Vector Regression (SVR)** - kernel methods

### 5.2 Advanced Models
- [ ] **LSTM/GRU Neural Networks** - cho time series patterns
- [ ] **Prophet** - Facebook's time series forecasting
- [ ] **ARIMA/SARIMA** - classical time series models
- [ ] **Ensemble methods** - stacking multiple models

### 5.3 Hyperparameter Tuning
- [ ] **Grid Search** hoặc **Bayesian Optimization**
- [ ] **Time Series Cross-validation** for robust evaluation
- [ ] **Feature importance analysis** từ tree-based models
- [ ] **Model interpretability** - SHAP values

---

## **BƯỚC 6: MODEL EVALUATION** 

### 6.1 Performance Metrics
- [ ] **RMSE** (Root Mean Square Error) - primary metric
- [ ] **MAE** (Mean Absolute Error) - robust to outliers
- [ ] **R²** (R-squared score) - explained variance
- [ ] **MAPE** (Mean Absolute Percentage Error) - relative error

### 6.2 Validation Strategy
- [ ] **Time-based validation** - train on past, test on future
- [ ] **Cross-validation** results analysis
- [ ] **Learning curves** - overfitting detection
- [ ] **Residual analysis** - error pattern detection

### 6.3 Visualization & Analysis
- [ ] **Predicted vs Actual** scatter plots
- [ ] **Time series comparison** - predicted vs actual over time
- [ ] **Feature importance** rankings và visualization
- [ ] **Error distribution** analysis

---

## **BƯỚC 7: MODEL DEPLOYMENT & PREDICTION** 

### 7.1 Final Model Selection
- [ ] **Model comparison table** với tất cả metrics
- [ ] **Best model selection** based on multiple criteria
- [ ] **Model ensemble** nếu cần thiết
- [ ] **Final model validation** trên test set

### 7.2 Prediction System
- [ ] **Real-time prediction function** 
- [ ] **Batch prediction** cho multiple time points
- [ ] **Confidence intervals** và uncertainty quantification
- [ ] **Prediction horizon:** 1h, 6h, 24h, 7 days ahead

### 7.3 Practical Applications
- [ ] **Air quality alert system** - warning thresholds
- [ ] **Health recommendations** based on PM2.5 levels
- [ ] **Outdoor activity planning** tool
- [ ] **Policy insights** cho environmental management

---

## **BƯỚC 8: DOCUMENTATION & REPORTING** 

### 8.1 Technical Documentation
- [ ] **Data pipeline documentation**
- [ ] **Model architecture** và parameters
- [ ] **Performance benchmarks** và comparison
- [ ] **Code documentation** và reproducibility

### 8.2 Business Report
- [ ] **Executive summary** với key findings
- [ ] **Model accuracy** và reliability assessment
- [ ] **Business impact** và cost-benefit analysis
- [ ] **Limitations** và future improvement recommendations

### 8.3 Visualization Dashboard
- [ ] **Real-time monitoring** dashboard
- [ ] **Historical trends** analysis
- [ ] **Prediction visualizations** 
- [ ] **Interactive exploration** tools

---

## **FINAL DELIVERABLES:**

###  **Core Outputs:**
1. **Production-ready model** với documented performance
2. **Prediction API/function** cho real-time forecasting  
3. **Comprehensive dataset** với engineered features
4. **Performance benchmark** comparison table

###  **Business Outputs:**  
5. **Air quality monitoring dashboard**
6. **Health advisory system** based on predictions
7. **Policy recommendations** report
8. **Future research directions** roadmap

###  **Documentation:**
9. **Technical documentation** đầy đủ
10. **User manual** cho prediction system
11. **Research paper/report** với methodology
12. **Presentation materials** cho stakeholders

---

## **TIMELINE & EFFORT ALLOCATION:**

| Giai đoạn | Thời gian | Effort % |
|-----------|-----------|----------|
| **Data Collection & Integration** | Week 1 | 15% |
| **EDA & Data Understanding** | Week 1-2 | 25% |
| **Data Preprocessing** | Week 2 | 20% |
| **Model Development** | Week 2-3 | 25% |
| **Evaluation & Tuning** | Week 3 | 10% |
| **Documentation & Deployment** | Week 4 | 5% |

---