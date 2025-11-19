# 📓 Notebooks Directory

Thư mục này chứa tất cả Jupyter notebooks để thực hiện pipeline PM2.5 Air Quality Prediction theo từng giai đoạn.

## 🔄 Execution Order

Chạy các notebooks theo thứ tự sau để đảm bảo pipeline hoạt động đúng:

### 1. Data Processing (Required)
**`G3_Assignment_Data_For_Train_Processing.ipynb`**
- Thu thập dữ liệu training từ Weatherbit API
- Xử lý và merge weather + air quality data
- Output: `../data/hanoi_weather_air_quality_final.csv`

### 2. Test Data Collection (Optional)
**`G3_Assignment_Data_For_Test.ipynb`**
- Thu thập dữ liệu test cho validation
- Output: `../data/hanoi_weather_air_quality_final_test_data.csv`

### 3. Model Training (Required) 
**`G3_Assignment_Model_Training.ipynb`**
- So sánh 6 machine learning algorithms
- Đánh giá hiệu quả trên original vs scaled data
- Output: `../models/best_pm25_model_*.pkl`, `../models/pm25_scaler.pkl`

### 4. Prediction (Required)
**`G3_Assignment_PM25_Prediction_7Days.ipynb`**
- Load trained models và tạo dự báo 7 ngày
- So sánh predictions với actual data (nếu có)
- Output: CSV files và visualizations

## 📋 Notebook Details

### Data Processing Notebooks

#### G3_Assignment_Data_For_Train_Processing.ipynb
**Purpose**: Thu thập và xử lý dữ liệu training

**Key Functions**:
- `get_weather_data()`: Lấy dữ liệu thời tiết từ API
- `get_air_quality_history()`: Lấy dữ liệu chất lượng không khí
- `merge_and_aggregate_final_data()`: Merge và tạo features

**Input Requirements**:
- Weatherbit API keys
- Khoảng thời gian cần thu thập

**Output**:
- `../data/hanoi_weather_history.csv`
- `../data/hanoi_air_quality_history.csv` 
- `../data/hanoi_weather_air_quality_final.csv`

#### G3_Assignment_Data_For_Test.ipynb
**Purpose**: Thu thập dữ liệu test cho validation

**Similar structure** như training notebook nhưng:
- Thu thập dữ liệu gần đây hơn
- Dùng để validate model predictions

### Model Training Notebook

#### G3_Assignment_Model_Training.ipynb
**Purpose**: Huấn luyện và so sánh các machine learning models

**Key Sections**:
1. **Data Loading & Preprocessing**
   - Load dữ liệu từ `../data/hanoi_weather_air_quality_final.csv`
   - Feature engineering và time features
   - Handle multicollinearity

2. **Model Comparison**
   - Random Forest, XGBoost, Linear Regression
   - So sánh trên original vs scaled data
   - Cross-validation và performance metrics

3. **Model Selection & Export**
   - Chọn best models dựa trên R² và RMSE
   - Save models và scaler vào `../models/`

**Dependencies**:
```python
pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn, joblib
```

### Prediction Notebook

#### G3_Assignment_PM25_Prediction_7Days.ipynb
**Purpose**: Tạo dự báo PM2.5 cho 7 ngày tiếp theo

**Key Sections**:
1. **Model Loading**
   - Load trained models từ `../models/`
   - Load historical data từ `../data/`

2. **Future Feature Generation**
   - Tạo time features cho 168 giờ tiếp theo (7 ngày × 24 giờ)
   - Sử dụng trung bình historical cho environmental features

3. **Prediction & Validation**
   - Generate predictions với cả 2 models (original & scaled)
   - So sánh với actual data nếu có
   - Tính toán error metrics

4. **Visualization & Analysis**
   - Time series plots
   - Hourly và daily patterns
   - Performance analysis

## 🔧 Setup Requirements

### Environment Setup
```bash
# Install required packages
pip install pandas numpy scikit-learn xgboost matplotlib seaborn requests joblib

# Start Jupyter
jupyter notebook
```

### API Configuration
Cần cấu hình API keys trong data processing notebooks:
```python
API_KEY = 'your_weatherbit_api_key_here'
API_KEY_BACKUP = 'your_backup_api_key_here'
```

### File Paths
Tất cả notebooks sử dụng relative paths:
- Data input: `../data/`
- Model output: `../models/`
- Relative imports được handle tự động

## 📊 Expected Runtime

| Notebook | Runtime | Notes |
|----------|---------|-------|
| Data Processing | 15-30 min | Depends on API speed |
| Test Data | 5-10 min | Smaller dataset |
| Model Training | 5-15 min | Depends on CPU |
| Prediction | 2-5 min | Fast inference |

## ⚠️ Troubleshooting

### Common Issues

1. **API Timeout**
   - Solution: Notebook tự động retry với exponential backoff
   - Alternative: Giảm khoảng thời gian thu thập data

2. **Memory Issues**  
   - Solution: Process data theo chunks
   - Minimum 4GB RAM recommended

3. **Missing Dependencies**
   - Solution: `pip install -r requirements.txt`

4. **Model Not Found**
   - Solution: Chạy Model Training notebook trước Prediction

### Performance Optimization

- **Parallel Processing**: Có thể chạy data collection notebooks song song
- **Caching**: Trained models được cache, không cần retrain
- **Incremental Updates**: Data collection hỗ trợ append mode

## 🎯 Output Validation

Sau khi chạy xong pipeline, check:
- [ ] `../data/hanoi_weather_air_quality_final.csv` exists và có >8000 rows
- [ ] `../models/best_pm25_model_*.pkl` files exist
- [ ] `../models/pm25_scaler.pkl` exists  
- [ ] Prediction notebook chạy không lỗi và tạo ra visualizations
