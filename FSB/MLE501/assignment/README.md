
# 🌦️ GlobalWeatherRepository Dataset

## 📘 Tổng quan
Bộ dữ liệu **GlobalWeatherRepository.csv** chứa thông tin thời tiết và chất lượng không khí của hơn **100,000 bản ghi** được thu thập từ nhiều quốc gia và khu vực trên toàn cầu.
Dữ liệu này rất hữu ích cho các bài toán **dự báo thời tiết**, **dự đoán mức độ ô nhiễm không khí**, hoặc **phân tích khí hậu**.

---

## 📊 Thông tin tổng quát
- **Số dòng:** 101,334
- **Số cột:** 41
- **Không có giá trị null**
- **Định dạng file:** CSV (UTF-8)

---

## 🧩 Cấu trúc dữ liệu

| Nhóm dữ liệu | Tên cột | Mô tả |
|---------------|----------|--------|
| **Địa lý** | `country`, `location_name`, `latitude`, `longitude`, `timezone` | Quốc gia, thành phố, tọa độ, múi giờ |
| **Thời gian cập nhật** | `last_updated_epoch`, `last_updated` | Thời điểm cập nhật dữ liệu (Unix timestamp và dạng đọc được) |
| **Nhiệt độ & cảm nhận** | `temperature_celsius`, `temperature_fahrenheit`, `feels_like_celsius`, `feels_like_fahrenheit` | Nhiệt độ thực tế và cảm nhận |
| **Điều kiện thời tiết** | `condition_text`, `humidity`, `cloud`, `uv_index`, `visibility_km`, `visibility_miles` | Mô tả thời tiết, độ ẩm, mây, tia UV, tầm nhìn |
| **Gió & áp suất** | `wind_mph`, `wind_kph`, `wind_degree`, `wind_direction`, `gust_mph`, `gust_kph`, `pressure_mb`, `pressure_in` | Tốc độ, hướng gió, và áp suất khí quyển |
| **Lượng mưa** | `precip_mm`, `precip_in` | Lượng mưa theo mm và inch |
| **Chất lượng không khí (Air Quality)** | `air_quality_Carbon_Monoxide`, `air_quality_Ozone`, `air_quality_Nitrogen_dioxide`, `air_quality_Sulphur_dioxide`, `air_quality_PM2.5`, `air_quality_PM10`, `air_quality_us-epa-index`, `air_quality_gb-defra-index` | Các thành phần hóa học và chỉ số AQI theo chuẩn Mỹ & Anh |
| **Thiên văn học** | `sunrise`, `sunset`, `moonrise`, `moonset`, `moon_phase`, `moon_illumination` | Giờ mặt trời mọc/lặn, trăng mọc/lặn, pha trăng, độ chiếu sáng trăng |

---

## 🔢 Kiểu dữ liệu
- **Chuỗi (Object):** 14 cột  
- **Số thực (float64):** 20 cột  
- **Số nguyên (int64):** 7 cột  

---

## 🧠 Ứng dụng gợi ý trong Machine Learning
1. **Dự đoán mức độ ô nhiễm không khí (Air Quality Prediction)**  
   - Mục tiêu: Dự đoán các chỉ số như `air_quality_PM2.5` hoặc `us-epa-index` dựa vào các yếu tố khí tượng.
2. **Phân loại điều kiện thời tiết (Weather Classification)**  
   - Dự đoán `condition_text` từ dữ liệu số.
3. **Phân cụm khí hậu toàn cầu (Global Climate Clustering)**  
   - Nhóm các khu vực có điều kiện khí hậu tương đồng.

---

## 📂 Ví dụ dữ liệu

| country | location_name | temperature_celsius | condition_text | humidity | air_quality_PM2.5 | air_quality_PM10 |
|----------|----------------|--------------------|----------------|-----------|-------------------|------------------|
| Afghanistan | Kabul | 26.6 | Partly Cloudy | 24 | 8.4 | 26.6 |
| Albania | Tirana | 19.0 | Partly cloudy | 94 | 1.1 | 2.0 |
| Algeria | Algiers | 23.0 | Sunny | 29 | 10.4 | 18.4 |
| Andorra | Andorra La Vella | 6.3 | Light drizzle | 61 | 0.7 | 0.9 |
| Angola | Luanda | 26.0 | Partly cloudy | 89 | 183.4 | 262.3 |

---

## 📅 Nguồn gốc và thời gian
- **Thời gian cập nhật mẫu:** tháng 5 năm 2024
- **Đơn vị đo:** quốc tế (SI units và Imperial units)
- **Nguồn gốc dự kiến:** dữ liệu tổng hợp từ API thời tiết toàn cầu (World Weather / WeatherAPI / OpenWeather)

---

## 📚 Gợi ý xử lý trước khi dùng (Preprocessing)
- Chuyển đổi cột thời gian (`last_updated`) sang dạng `datetime` chuẩn.
- Mã hóa các biến phân loại như `condition_text`, `country`, `wind_direction` bằng OneHot hoặc Label Encoding.
- Chuẩn hóa dữ liệu số bằng MinMaxScaler hoặc StandardScaler nếu dùng cho mô hình ML.

---

## 🧾 Thông tin thêm
Tác giả/thu thập: **GlobalWeatherRepository (open dataset)**  
Phiên bản: 1.0  
Ngày phân tích: 2025-10-20

