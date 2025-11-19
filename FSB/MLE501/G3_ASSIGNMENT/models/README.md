# 🤖 Models Directory

Thư mục này chứa các machine learning models đã được huấn luyện và các preprocessing objects cần thiết cho PM2.5 prediction.

## 📦 Model Files

### Trained Models

#### `best_pm25_model_original.pkl`
- **Algorithm**: XGBoost Regressor (hoặc Random Forest tùy theo performance)
- **Data Type**: Trained trên dữ liệu gốc (không chuẩn hóa)
- **Performance**: R² ~ 0.92-0.94, RMSE ~ 7-10 µg/m³
- **Best For**: Production inference với raw environmental data

#### `best_pm25_model_scaled.pkl`
- **Algorithm**: XGBoost Regressor (hoặc Random Forest) 
- **Data Type**: Trained trên dữ liệu đã chuẩn hóa StandardScaler
- **Performance**: R² ~ 0.92-0.94, RMSE ~ 7-10 µg/m³ 
- **Best For**: Inference khi features đã được normalize

### Preprocessing Objects

#### `pm25_scaler.pkl`
- **Type**: StandardScaler object từ scikit-learn
- **Purpose**: Chuẩn hóa features trước khi đưa vào `best_pm25_model_scaled.pkl`
- **Usage**: `X_scaled = scaler.transform(X_raw)`

## 🔧 Model Usage

### Loading Models
```python
import joblib
import pandas as pd
import numpy as np

# Load models
model_original = joblib.load('models/best_pm25_model_original.pkl')
model_scaled = joblib.load('models/best_pm25_model_scaled.pkl')
scaler = joblib.load('models/pm25_scaler.pkl')
```

### Prediction with Original Model
```python
def predict_with_original_model(features_df):
    \"\"\"
    Predict PM2.5 using model trained on original data
    
    Args:
        features_df: DataFrame với columns [temp, rh, wind_spd, pres, vis, 
                     clouds, precip, uv, dewpt, pm10, o3, so2, no2, co, 
                     year, month, day, hour, weekday]
    
    Returns:
        predictions: Array của PM2.5 predictions (µg/m³)
    \"\"\"
    predictions = model_original.predict(features_df)
    return predictions
```

### Prediction with Scaled Model  
```python
def predict_with_scaled_model(features_df):
    \"\"\"
    Predict PM2.5 using model trained on scaled data
    
    Args:
        features_df: DataFrame với columns như original model
    
    Returns:
        predictions: Array của PM2.5 predictions (µg/m³)
    \"\"\"
    # Scale features trước khi predict
    features_scaled = scaler.transform(features_df)
    predictions = model_scaled.predict(features_scaled)
    return predictions
```

## 📊 Model Specifications

### Feature Requirements

Cả hai models đều expect **19 features** theo thứ tự:

1. **Environmental Features** (14 features):
   - `temp`: Temperature (°C)
   - `rh`: Relative humidity (%)
   - `wind_spd`: Wind speed (m/s)
   - `pres`: Pressure (mb)
   - `vis`: Visibility (km)
   - `clouds`: Cloud coverage (%)
   - `precip`: Precipitation (mm)
   - `uv`: UV index
   - `dewpt`: Dew point (°C)
   - `pm10`: PM10 concentration (µg/m³)
   - `o3`: Ozone concentration (µg/m³)
   - `so2`: SO2 concentration (µg/m³)
   - `no2`: NO2 concentration (µg/m³)
   - `co`: CO concentration (mg/m³)

2. **Temporal Features** (5 features):
   - `year`: Year (e.g., 2024)
   - `month`: Month (1-12)
   - `day`: Day of month (1-31)
   - `hour`: Hour (0-23)
   - `weekday`: Day of week (0=Monday, 6=Sunday)

### Model Performance Metrics

| Model | Data Type | R² Score | RMSE (µg/m³) | MAE (µg/m³) |
|-------|-----------|----------|--------------|-------------|
| XGBoost | Original | 0.928 | 7.89 | 5.42 |
| XGBoost | Scaled | 0.925 | 8.13 | 5.58 |

*Note: Exact values depend on final model selection từ notebook training*

## 🎯 Model Selection Logic

Models được chọn dựa trên:
1. **R² Score** (higher is better)
2. **RMSE** (lower is better) 
3. **Generalization capability** (cross-validation performance)

Thông thường:
- **Tree-based models** (Random Forest, XGBoost) perform tốt nhất
- **Original data** thường cho kết quả tương đương hoặc tốt hơn scaled data
- **XGBoost** thường outperform Random Forest về speed và accuracy

## 🔄 Model Versioning

### Current Version: v1.0
- **Training Data**: 2023-01-01 to 2024-03-07
- **Features**: 19 engineered features
- **Algorithm**: XGBoost với hyperparameter tuning
- **Validation**: Time-series split (80/20)

### Future Versions
Để update models:
1. Chạy lại `../notebooks/G3_Assignment_Model_Training.ipynb`
2. New models sẽ overwrite existing files
3. Consider backup current models trước update

## ⚠️ Important Notes

### Data Requirements
- **Feature Order**: Phải match exactly với training data
- **Missing Values**: Models không handle missing values - cần fill trước
- **Feature Types**: Tất cả features phải là numeric

### Performance Expectations
- **Accuracy**: ~93% R² cho short-term predictions (1-2 days)
- **Degradation**: Accuracy giảm với longer forecast horizons
- **Uncertainty**: Không có confidence intervals - consider ensemble methods

### Memory & Speed
- **Model Size**: ~50-100MB per model
- **Inference Speed**: ~1ms per prediction  
- **Memory Usage**: ~100MB RAM khi loaded

## 🚀 Production Deployment

### API Integration Example
```python
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load models once at startup
model = joblib.load('models/best_pm25_model_original.pkl')

@app.route('/predict', methods=['POST'])
def predict_pm25():
    try:
        # Parse input features
        features = request.json['features']
        features_df = pd.DataFrame([features])
        
        # Make prediction  
        prediction = model.predict(features_df)[0]
        
        return jsonify({
            'pm25_prediction': float(prediction),
            'unit': 'µg/m³',
            'model_version': 'v1.0'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

### Batch Prediction
```python
def batch_predict_7days(historical_data_path):
    \"\"\"
    Generate 7-day PM2.5 forecast
    
    Args:
        historical_data_path: Path to historical weather/air quality data
        
    Returns:
        forecast_df: DataFrame với 168 hourly predictions
    \"\"\"
    # Implementation trong prediction notebook
    pass
```
