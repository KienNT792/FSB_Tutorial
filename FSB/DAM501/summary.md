# Tổng hợp pipeline & kết quả dự báo PM2.5 Hà Nội

## Mục tiêu
- Dự báo PM2.5 đa bước (1h, 2h, 4h, 6h, 12h, 24h).
- Kết hợp chất lượng không khí, thời tiết, ngày lễ, giao thông.

## Dữ liệu nguồn
- `data/data_file/hanoi_air_quality_history.csv` (25,429 dòng; datetime `%Y-%m-%d:%H`; 2022-12-31 17:00 → 2025-12-29 11:00)
- `data/data_file/hanoi_weather_history.csv` (25,393 dòng; datetime `%Y-%m-%d:%H`; 2022-12-31 17:00 → 2025-12-29 04:00)
- `data/data_file/hanoi_holidays_aligned.csv` (24,024 dòng; datetime `%Y-%m-%d %H:%M:%S`; 2022-12-31 17:00 → 2025-10-30 16:00)
- `data/data_file/hanoi_traffic_proxy.csv` (24,816 dòng; datetime `%Y-%m-%d %H:%M:%S`; 2022-12-31 17:00 → 2025-10-30 16:00)

## Pipeline xử lý
- Chuẩn hóa datetime, merge: air + weather (inner), holidays + traffic (left).
- Làm sạch:
  - `is_holiday` thiếu → 0; `holiday_name` thiếu → rỗng.
  - `congestion_index` thiếu → median; `congestion_noise` thiếu → 0.
- Sắp xếp theo thời gian và kiểm tra thống kê.

## EDA chính
- Missing values: `congestion_index` 1,368 (5.39%), `vis` 7 (0.03%).
- Ngày lễ: 717 giờ (2.8%); thường 24,675 giờ (97.2%).
  - Tết Nguyên Đán 480h, Tết Dương Lịch 72h, 30/4 21h, 1/5 72h, Quốc Khánh 72h.
- Giao thông: `congestion_index` mean 60.4, min 10.0, max 100.0, std 15.2; `congestion_noise` mean 0.02, std 1.96.

## Feature engineering
- Thời gian: `hour`, `day_of_week`, `month`, `day`.
- Cyclic: `hour_sin/cos`, `month_sin/cos`.
- Gió: `wind_dir` → `wind_dir_sin/cos`.
- Lag: `pm25`, `temp`, `wind_spd` tại [1, 3, 6, 12, 24, 48, 72]h.
- Rolling (pm25): mean/std/min/max cửa sổ [6, 12, 24, 48]h.
- Diff: `pm25_diff_1h`, `pm25_diff_24h`, `temp_diff_1h`.
- Categorical: `is_peak_hour`, `is_night`, `is_weekend`.
- Interaction: `temp_x_rh`, `wind_spd_x_temp`.
- Sau FE: 23,945 dòng, 77 cột.

## Modeling & đánh giá
- Models: XGBoost, LightGBM, CatBoost; 6 horizons; 18 model.
- Dữ liệu train/test: 19,155 / 4,789 mẫu; số feature dùng cho model: 74.
- Best overall: LightGBM 1h, R² 0.5921, RMSE 15.34, MAE 8.21.
- Avg theo model:
  - XGBoost R² 0.3389 | RMSE 19.37 | MAE 11.86
  - LightGBM R² 0.3376 | RMSE 19.38 | MAE 11.79
  - CatBoost R² 0.3407 | RMSE 19.34 | MAE 11.73
- XGBoost theo horizon:
  - 1h R² 0.5914 | RMSE 15.36 | MAE 8.23
  - 2h R² 0.4750 | RMSE 17.41 | MAE 9.76
  - 4h R² 0.3553 | RMSE 19.29 | MAE 11.69
  - 6h R² 0.2918 | RMSE 20.21 | MAE 12.64
  - 12h R² 0.1918 | RMSE 21.57 | MAE 13.93
  - 24h R² 0.1283 | RMSE 22.37 | MAE 14.93
- Insight: R² ngắn hạn (≤6h) 0.4283; dài hạn (>6h) 0.1600; suy giảm 62.6%.
- Khuyến nghị: 1–2h tin cậy cao; 4–6h trung bình; 12–24h chỉ nên tham khảo.

## Output/Artifacts
- Model: `data/notebook/output/{model}_model_*h.pkl`
- Metrics: `data/notebook/output/all_models_results.csv`
- Predictions: `data/notebook/output/all_predictions.csv`
- Visualizations: `data/notebook/output/*.png` (ví dụ `data/notebook/output/pm25_analysis.png`)

## Ghi chú phạm vi
- Dải thời gian air/weather kéo dài tới 2025-12, trong khi holiday/traffic tới 2025-10.
- Một số missing ở `vis` và `congestion_index`; dữ liệu lag/rolling được dropna sau FE.
