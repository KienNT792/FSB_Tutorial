# 📁 Data Directory

Thư mục này chứa tất cả dữ liệu raw và processed được sử dụng trong project PM2.5 Air Quality Prediction.

## 📊 Cấu Trúc Dữ Liệu

### Training Data Files
- **`hanoi_weather_history.csv`**: Dữ liệu thời tiết lịch sử từ Weatherbit API
- **`hanoi_air_quality_history.csv`**: Dữ liệu chất lượng không khí lịch sử  
- **`hanoi_weather_air_quality_final.csv`**: Dữ liệu training đã merge và xử lý

### Test Data Files
- **`hanoi_weather_history_test_data.csv`**: Dữ liệu thời tiết test
- **`hanoi_air_quality_history_test_data.csv`**: Dữ liệu chất lượng không khí test
- **`hanoi_weather_air_quality_final_test_data.csv`**: Dữ liệu test đã merge và xử lý

### Samples Directory
- **`samples/`**: Chứa các file JSON mẫu response từ Weatherbit API

## 📋 Data Schema

### Weather Data Columns
- `datetime`: Timestamp (YYYY-MM-DD HH:MM:SS)
- `temp`: Nhiệt độ (°C)
- `app_temp`: Nhiệt độ cảm nhận (°C)
- `rh`: Độ ẩm tương đối (%)
- `wind_spd`: Tốc độ gió (m/s)
- `wind_dir`: Hướng gió (độ)
- `pres`: Áp suất khí quyển (mb)
- `vis`: Tầm nhìn (km)
- `clouds`: Độ che phủ mây (%)
- `precip`: Lượng mưa (mm)
- `uv`: Chỉ số UV
- `dewpt`: Điểm sương (°C)

### Air Quality Data Columns
- `datetime`: Timestamp (YYYY-MM-DD HH:MM:SS)
- `aqi`: Air Quality Index (0-500)
- `pm25`: PM2.5 concentration (µg/m³) - **TARGET VARIABLE**
- `pm10`: PM10 concentration (µg/m³)
- `o3`: Ozone concentration (µg/m³)
- `so2`: SO2 concentration (µg/m³)
- `no2`: NO2 concentration (µg/m³)
- `co`: CO concentration (mg/m³)

### Final Dataset Features
- **Time features**: `year`, `month`, `day`, `hour`, `weekday`
- **Weather features**: 12 environmental variables
- **Air quality features**: 6 pollution indicators
- **Total**: ~19 features sau khi xử lý

## 🔄 Data Processing Pipeline

1. **Collection**: Thu thập từ Weatherbit API theo từng tháng
2. **Cleaning**: Xử lý missing values, format datetime
3. **Merging**: Kết hợp weather và air quality data theo timestamp
4. **Feature Engineering**: Tạo time features, xử lý multicollinearity
5. **Validation**: Kiểm tra data quality và consistency

## 📈 Data Statistics

### Temporal Coverage
- **Period**: 2023-01-01 đến 2025-11-01 (training)
- **Frequency**: Hourly measurements
- **Total Records**: 8,000+ cho training data

### Data Quality
- **Completeness**: >95% cho các features quan trọng
- **Consistency**: Timestamps được chuẩn hóa và validate
- **Outliers**: Được phát hiện và xử lý trong modeling phase

## ⚠️ Important Notes

- Dữ liệu được thu thập từ Weatherbit API - cần API key để reproduce
- File `hanoi_weather_air_quality_final.csv` là input chính cho model training
- Test data được sử dụng để validate model predictions trong thời gian thực
- Tất cả timestamps đều ở timezone địa phương (UTC+7 cho Hà Nội)
