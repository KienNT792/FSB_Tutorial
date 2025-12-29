# 🌫️ Hệ Thống Dự Báo PM2.5 Hà Nội - 1 Giờ Tới

## 📋 Mô Tả

Script tự động dự đoán nồng độ PM2.5 cho 1 giờ tới dựa trên:
- ✅ Dữ liệu lịch sử không khí (PM2.5, PM10, O3, SO2, NO2, CO)
- ✅ Dữ liệu thời tiết (nhiệt độ, độ ẩm, gió, áp suất, v.v.)
- ✅ Dữ liệu giao thông (chỉ số tắc nghẽn)
- ✅ Dữ liệu ngày lễ

## 🚀 Cách Sử Dụng

### 1. Chạy Script Dự Đoán

```bash
cd /Users/tungld/Documents/Code/FSB_Tutorial/FSB/DAM501/data/crawl_modules
python predict_next_hour.py
```

### 2. Kết Quả Hiển Thị

Script sẽ hiển thị:
- 📍 **Hiện tại**: PM2.5 hiện tại và mức độ chất lượng không khí
- 🔮 **Dự đoán**: PM2.5 dự đoán cho 1 giờ tới
- 📊 **Thay đổi**: Mức độ tăng/giảm so với hiện tại
- 💡 **Khuyến nghị**: Lời khuyên dựa trên mức độ ô nhiễm

### 3. Cập Nhật Dữ Liệu

Để có dự đoán chính xác nhất, cập nhật dữ liệu định kỳ:

```bash
# Cập nhật dữ liệu hàng tháng
python update_monthly_data.py

# Hoặc cập nhật dữ liệu hiện tại (nếu có API key)
python update_current_data.py
```

## 📊 Mức Độ Chất Lượng Không Khí (AQI)

| PM2.5 (μg/m³) | Mức Độ | Màu Sắc | Khuyến Nghị |
|---------------|--------|---------|-------------|
| 0 - 12 | TỐT | 🟢 Xanh | An toàn cho mọi người |
| 12.1 - 35.4 | TRUNG BÌNH | 🔵 Xanh dương | Chấp nhận được |
| 35.5 - 55.4 | KÉM | 🟡 Vàng | Nhóm nhạy cảm nên hạn chế ra ngoài |
| 55.5 - 150.4 | XẤU | 🔴 Đỏ | Hạn chế ra ngoài, đeo khẩu trang |
| 150.5 - 250.4 | RẤT XẤU | 🔴 Đỏ đậm | Tránh ra ngoài |
| > 250.4 | NGUY HIỂM | 🔴 Đỏ | Nguy hiểm, ở trong nhà |

## 🤖 Thông Tin Mô Hình

### Mô Hình Sử Dụng
- **Loại**: XGBoost Regressor
- **Horizon**: 1 giờ
- **R² Score**: ~0.754
- **MAE**: ~8.71 μg/m³
- **RMSE**: ~13.44 μg/m³

### Đặc Trưng Sử Dụng (73 features)
1. **Time Features** (8): hour, day_of_week, month, cyclical encoding
2. **Lag Features** (28): PM2.5, nhiệt độ, gió, giao thông (lags: 1, 3, 6, 12, 24, 48, 72h)
3. **Rolling Statistics** (16): mean, std, min, max cho windows 6, 12, 24, 48h
4. **Difference Features** (3): PM2.5 và nhiệt độ differences
5. **Categorical Features** (5): peak hour, night, weekend, high/low traffic
6. **Interaction Features** (5): temp×humidity, wind×temp, traffic interactions
7. **Raw Features** (8): PM10, O3, SO2, NO2, CO, temp, humidity, wind, pressure, v.v.

## 📂 Cấu Trúc File

```
data/
├── crawl_modules/
│   ├── predict_next_hour.py      # ⭐ Script dự đoán chính
│   ├── update_monthly_data.py     # Cập nhật dữ liệu hàng tháng
│   ├── update_current_data.py     # Cập nhật dữ liệu hiện tại
│   └── README_PREDICTION.md       # File này
├── data_file/
│   ├── hanoi_air_quality_history.csv
│   ├── hanoi_weather_history.csv
│   ├── hanoi_holidays_aligned.csv
│   └── hanoi_traffic_proxy.csv
└── notebook/
    └── output/
        └── xgboost_model_1h.pkl   # Model đã huấn luyện
```

## 🔧 Tùy Chỉnh

### Sử Dụng Model Khác

Trong file `predict_next_hour.py`, thay đổi:

```python
# Dòng 16-18
MODEL_FILE = 'xgboost_model_1h.pkl'  # Mặc định

# Có thể đổi thành:
MODEL_FILE = 'lightgbm_model_1h.pkl'  # LightGBM (R²=0.7544)
MODEL_FILE = 'catboost_model_1h.pkl'  # CatBoost (R²=0.7550) - Tốt nhất
```

### Bật Cập Nhật Real-time

Bỏ comment dòng 289-292 trong `predict_next_hour.py`:

```python
# Lấy dữ liệu real-time từ API
current_data = fetch_current_data()
if current_data is None:
    print_warning("Không thể lấy dữ liệu real-time, sử dụng dữ liệu lịch sử")
```

**Lưu ý**: Cần có API key hợp lệ và quota

## 📈 Hiệu Suất Mô Hình

### So Sánh Các Mô Hình (1h forecast)

| Model | R² Score | RMSE | MAE |
|-------|----------|------|-----|
| **CatBoost** | **0.7550** | **13.38** | **8.69** |
| LightGBM | 0.7544 | 13.40 | 8.70 |
| XGBoost | 0.7543 | 13.44 | 8.71 |

### Hiệu Suất Theo Horizon

| Horizon | R² Score | MAE | Độ Tin Cậy |
|---------|----------|-----|------------|
| 1h | 0.754 | 8.7 | ⭐⭐⭐⭐⭐ CAO |
| 2h | 0.724 | 9.8 | ⭐⭐⭐⭐⭐ CAO |
| 4h | 0.664 | 11.6 | ⭐⭐⭐⭐ TRUNG BÌNH |
| 6h | 0.540 | 13.7 | ⭐⭐⭐ TRUNG BÌNH |
| 12h | 0.376 | 16.2 | ⭐⭐ THẤP |
| 24h | 0.325 | 17.3 | ⭐⭐ THẤP |

## 🔄 Tự Động Hóa

### Chạy Định Kỳ với Cron

```bash
# Mở crontab
crontab -e

# Chạy mỗi giờ vào phút thứ 5
5 * * * * cd /path/to/crawl_modules && /path/to/.venv/bin/python predict_next_hour.py >> /path/to/logs/prediction.log 2>&1

# Cập nhật dữ liệu hàng ngày lúc 2h sáng
0 2 * * * cd /path/to/crawl_modules && /path/to/.venv/bin/python update_current_data.py >> /path/to/logs/update.log 2>&1
```

## 📞 Hỗ Trợ

### Các Vấn Đề Thường Gặp

**1. Lỗi "No module named 'xgboost'"**
```bash
pip install xgboost
```

**2. Lỗi "FileNotFoundError: model not found"**
- Kiểm tra model đã được train chưa
- Chạy notebook `pm25_multi_horizon_forecast_notebook.ipynb` để train model

**3. Dữ liệu quá cũ**
```bash
# Cập nhật dữ liệu
python update_monthly_data.py
```

**4. Kết quả không chính xác**
- Cập nhật dữ liệu mới nhất
- Kiểm tra feature engineering có giống với training không
- Thử model khác (CatBoost hoặc LightGBM)

## 📝 License

MIT License - Tự do sử dụng và chỉnh sửa

## 👨‍💻 Tác Giả

DAM501 Project - PM2.5 Forecasting System for Hanoi
