# Báo cáo cải thiện pipeline dự báo PM2.5 Hà Nội

## 1) Tình trạng hiện tại (tóm tắt nhanh)
- Nguồn dữ liệu: air quality, weather, holidays, traffic (theo giờ).
- Đã merge + feature engineering (lag/rolling/cyclic/time/categorical/interaction).
- Mô hình: XGBoost/LightGBM/CatBoost, dự báo 1–24h.

## 2) Phân tích tiền xử lý (external)
- Báo cáo chi tiết: `data/analysis/preprocessing/preprocess_report.md`
- Script sinh báo cáo: `data/analysis/preprocessing/generate_preprocess_report.py`

**Một số phát hiện chính:**
- Dải thời gian không đồng bộ: air/weather dài hơn holidays/traffic.
- Có khoảng trống giờ (gaps) ở air/weather/holidays; traffic đầy đủ hơn.
- `holiday_name` thiếu nhiều là bình thường (chỉ có ở ngày lễ).

## 3) Đề xuất cải thiện tiền xử lý
1) **Căn chỉnh thời gian**: cắt về khoảng giao nhau của tất cả nguồn (hoặc ít nhất air+weather+traffic).
2) **Kiểm tra gaps**: liệt kê/điền thiếu (forward-fill/linear) cho biến khí tượng; không nội suy cho biến nhị phân (is_holiday).
3) **Xử lý thiếu có điều kiện**:
   - `congestion_index`: dùng median theo giờ/ngày thay vì global median.
   - `vis`: có thể nội suy theo thời gian hoặc theo `rh`/`precip`.
4) **Chuẩn hóa lại datetime**: thống nhất format trước merge để tránh lệch giờ.
5) **Kiểm tra trùng lặp**: nếu có duplicate datetime, chọn bản ghi mới nhất hoặc aggregate.

## 4) Nguồn dữ liệu bổ sung (gợi ý)
- **Trạm AQ chính thức** (MONRE/địa phương) hoặc mạng cảm biến mở (PurpleAir).
- **Vệ tinh AOD**: MODIS/MAIAC, Sentinel-5P (tăng độ phủ không gian).
- **Dữ liệu khí tượng dự báo**: ERA5/GFS/ECMWF để dự báo dài hạn.
- **Nguồn phát thải**: công nghiệp, giao thông, cháy rừng (VIIRS active fires).
- **Hạ tầng & dân số**: mật độ đường, mật độ dân cư, land-use.
- **Traffic real-time**: TomTom/Google/Here (nếu truy cập được).

## 5) Đề xuất cải thiện mô hình
- **Time-series split** thay vì random split, kiểm tra drift theo năm/mùa.
- **Horizon-specific models** (direct) + ensemble thay vì một mô hình chung.
- **Hyperparameter tuning** (Optuna/RandomSearch) theo từng horizon.
- **Feature selection**: SHAP/feature importance, loại bỏ feature nhiễu.
- **Thử baseline TS**: SARIMA/Prophet để so sánh ngắn hạn.

## 6) Gợi ý trình bày kết quả
- Bảng so sánh metrics theo horizon + heatmap.
- Đồ thị lỗi theo mùa/giờ/ngày trong tuần.
- Phân tích suy giảm hiệu năng theo horizon (degradation curve).

---
Nếu bạn muốn, mình có thể triển khai trực tiếp các cải thiện trên vào notebook.
