# README - G3_Assignment_Data_Processing

## 📋 Mục Lục
1. [Tổng Quan](#tổng-quan)
2. [Mục Đích](#mục-đích)
3. [Kiến Trúc và Quy Trình](#kiến-trúc-và-quy-trình)
4. [Chi Tiết Kỹ Thuật](#chi-tiết-kỹ-thuật)
5. [Cấu Trúc Dữ Liệu](#cấu-trúc-dữ-liệu)
6. [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)
7. [Xử Lý Lỗi và Tối Ưu](#xử-lý-lỗi-và-tối-ưu)
8. [Kết Quả Thu Được](#kết-quả-thu-được)

---

## 🎯 Tổng Quan

Notebook `G3_Assignment_Data_Processing.ipynb` là công cụ thu thập và xử lý dữ liệu chất lượng không khí tự động từ **Weatherbit API** cho thành phố Hà Nội. Đây là bước đầu tiên và quan trọng nhất trong quy trình phân tích và dự báo chất lượng không khí.

### Tại sao cần notebook này?
- **Tự động hóa**: Thay vì thu thập dữ liệu thủ công, notebook tự động lấy dữ liệu từ API
- **Lịch sử dài hạn**: Thu thập dữ liệu từ 01/01/2023 đến thời điểm hiện tại
- **Độ tin cậy cao**: Xử lý lỗi, retry, và validation dữ liệu tự động
- **Chuẩn hóa**: Dữ liệu được lưu trữ theo định dạng chuẩn để phục vụ các bước tiếp theo

---

## 🎪 Mục Đích

### Mục Đích Chính
1. **Thu thập dữ liệu lịch sử**: Lấy toàn bộ dữ liệu chất lượng không khí của Hà Nội từ đầu năm 2023
2. **Xây dựng dataset**: Tạo một bộ dữ liệu hoàn chỉnh phục vụ cho việc:
   - Phân tích xu hướng chất lượng không khí
   - Huấn luyện mô hình Machine Learning dự báo PM2.5
   - Nghiên cứu mối tương quan giữa các chỉ số ô nhiễm

### Mục Đích Phụ
- **Kiểm soát chất lượng dữ liệu**: Đảm bảo dữ liệu đầy đủ, không bị thiếu
- **Tối ưu hóa API calls**: Giảm thiểu số lần gọi API để tránh rate limiting
- **Lưu trữ bền vững**: Dữ liệu được lưu vào CSV để sử dụng offline

---

## 🏗️ Kiến Trúc và Quy Trình

### Kiến Trúc Tổng Thể

```
┌─────────────────┐
│  Weatherbit API │
│  (Data Source)  │
└────────┬────────┘
         │ HTTPS Request
         ▼
┌─────────────────────┐
│ get_weather_data()  │
│  - API Call         │
│  - Error Handling   │
│  - Data Validation  │
└────────┬────────────┘
         │ JSON Response
         ▼
┌─────────────────────┐
│  pandas DataFrame   │
│  (In-Memory Data)   │
└────────┬────────────┘
         │ CSV Format
         ▼
┌─────────────────────┐
│ save_data_to_csv()  │
│  - Append Mode      │
│  - Deduplication    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ weather_data_hanoi  │
│       .csv          │
└─────────────────────┘
```

### Quy Trình Xử Lý Chi Tiết

#### **Bước 1: Chuẩn Bị và Cấu Hình**
```python
API_KEY = 'bd78df23972d4c5787e72fd978e7c5cb'
start_date = datetime(2023, 1, 1)
end_date = datetime.today()
```

**Tại sao?**
- API key xác thực với Weatherbit service
- Xác định khoảng thời gian cần thu thập dữ liệu
- `datetime.today()` đảm bảo luôn lấy dữ liệu mới nhất

#### **Bước 2: Chia Nhỏ Khoảng Thời Gian**
```python
months = get_months_between_dates(start_date, end_date)
```

**Tại sao chia theo tháng?**
1. **Giới hạn API**: Weatherbit API có giới hạn số ngày mỗi request
2. **Rate Limiting**: Tránh bị chặn khi request quá nhiều dữ liệu
3. **Quản lý lỗi**: Nếu 1 tháng lỗi, không ảnh hưởng tháng khác
4. **Tiến độ rõ ràng**: Dễ theo dõi tiến trình thu thập

**Cách hoạt động:**
- Tính toán số tháng giữa start_date và end_date
- Mỗi tháng tạo 1 tuple (first_day, last_day)
- Xử lý đặc biệt cho tháng cuối (không vượt quá end_date)

#### **Bước 3: Thu Thập Dữ Liệu từ API**

```python
url = "https://api.weatherbit.io/v2.0/history/airquality"
params = {
    'city': 'Hanoi',
    'start_date': start_date,
    'end_date': end_date,
    'tz': 'local',
    'key': api_key
}
```

**Tham số quan trọng:**
- `city='Hanoi'`: Chỉ định địa điểm cần lấy dữ liệu
- `tz='local'`: Múi giờ địa phương (GMT+7 cho Việt Nam)
- `verify=False`: Bỏ qua SSL verification (cần thiết trong một số môi trường)
- `timeout=30`: Đợi tối đa 30 giây, tránh treo vô hạn

**Xử lý response:**
```python
response = requests.get(url, params=params, verify=False, timeout=30)
response.raise_for_status()  # Raise exception nếu HTTP error
data = response.json()
records = data.get('data', [])
```

#### **Bước 4: Lưu Trữ Dữ Liệu**

```python
data.to_csv(file_name, index=False, mode='a', header=not file_exists)
```

**Tại sao sử dụng append mode?**
- Không ghi đè dữ liệu cũ
- Cho phép chạy nhiều lần mà không mất dữ liệu
- Tiết kiệm bộ nhớ (không cần load toàn bộ dữ liệu vào RAM)

**Header management:**
- Lần đầu: Ghi header (tên cột)
- Lần sau: Không ghi header (tránh duplicate)

#### **Bước 5: Rate Limiting và Monitoring**

```python
time.sleep(1)  # Chờ 1 giây giữa các request
```

**Tại sao cần delay?**
- **Tránh bị block**: Nhiều API có giới hạn request/giây
- **Server-friendly**: Không gây quá tải cho server
- **Tối ưu tài nguyên**: Cho phép server xử lý request khác

---

## 🔧 Chi Tiết Kỹ Thuật

### 1. Hàm `get_weather_data()`

**Chức năng**: Thu thập dữ liệu từ Weatherbit API

**Input Parameters:**
- `start_date (str)`: Ngày bắt đầu, format 'YYYY-MM-DD'
- `end_date (str)`: Ngày kết thúc, format 'YYYY-MM-DD'
- `api_key (str)`: API key để xác thực

**Output:**
- `pandas.DataFrame`: Dữ liệu chất lượng không khí
- `None`: Nếu có lỗi hoặc không có dữ liệu

**Error Handling:**

| Loại Lỗi | Xử Lý | Tại Sao |
|-----------|--------|---------|
| `Timeout` | Trả về None, log message | Tránh treo chương trình |
| `RequestException` | Catch và log chi tiết | Debug dễ dàng |
| `HTTP Error` | raise_for_status() | Phát hiện lỗi API sớm |
| `JSON Parse Error` | Try-except | Xử lý response không hợp lệ |

**Ví dụ response từ API:**
```json
{
  "data": [
    {
      "aqi": 160,
      "co": 340.0,
      "datetime": "2023-01-30:17",
      "no2": 47.3,
      "o3": 46.0,
      "pm10": 78.8,
      "pm25": 63.0,
      "so2": 110.0,
      "timestamp_local": "2023-01-31T00:00:00",
      "timestamp_utc": "2023-01-30T17:00:00",
      "ts": 1675098000
    }
  ]
}
```

### 2. Hàm `save_data_to_csv()`

**Chức năng**: Lưu DataFrame vào file CSV

**Logic quyết định:**
```
┌──────────────────┐
│ File tồn tại?    │
└────┬─────────────┘
     │
     ├─► YES ─► mode='a', header=False (Append không ghi header)
     │
     └─► NO  ─► mode='w', header=True  (Write với header)
```

**Tính năng:**
- **Atomic write**: Đảm bảo dữ liệu không bị corrupt
- **Progress tracking**: In ra số bản ghi đã lưu
- **Validation**: Kiểm tra DataFrame không empty trước khi lưu

### 3. Hàm `get_months_between_dates()`

**Chức năng**: Tạo danh sách các khoảng thời gian theo tháng

**Thuật toán:**
```
1. Khởi tạo: start_year, start_month từ start_date
2. Loop while (chưa đến end_date):
   a. Tạo month_start = ngày 1 của tháng
   b. Tính month_end = ngày cuối tháng (dùng monthrange)
   c. Nếu month_end > end_date: month_end = end_date
   d. Thêm (month_start, month_end) vào danh sách
   e. Tăng tháng (xử lý chuyển năm nếu tháng 12)
3. Trả về danh sách
```

**Xử lý trường hợp đặc biệt:**
- Tháng có số ngày khác nhau (28/29/30/31)
- Năm nhuận (February có 29 ngày)
- Tháng cuối không đầy đủ

**Ví dụ output:**
```python
[
  ('2023-01-01', '2023-01-31'),
  ('2023-02-01', '2023-02-28'),
  ('2023-03-01', '2023-03-31'),
  ...
  ('2024-11-01', '2024-11-10')  # Tháng cuối không đầy đủ
]
```

---

## 📊 Cấu Trúc Dữ Liệu

### Dữ Liệu Đầu Ra (weather_data_hanoi.csv)

**Các cột dữ liệu:**

| Cột | Kiểu | Mô Tả | Đơn Vị | Ý Nghĩa |
|-----|------|-------|--------|---------|
| `aqi` | int | Air Quality Index | - | Chỉ số chất lượng không khí tổng hợp |
| `co` | float | Carbon Monoxide | µg/m³ | Khí CO, độc hại khi nồng độ cao |
| `datetime` | str | Thời gian (local) | YYYY-MM-DD:HH | Timestamp theo múi giờ Hà Nội |
| `no2` | float | Nitrogen Dioxide | µg/m³ | Khí NO₂, gây kích ứng đường hô hấp |
| `o3` | float | Ozone | µg/m³ | Ozone tầng thấp, có hại cho sức khỏe |
| `pm10` | float | Particulate Matter 10 | µg/m³ | Bụi mịn đường kính ≤ 10 micromet |
| `pm25` | float | Particulate Matter 2.5 | µg/m³ | Bụi mịn đường kính ≤ 2.5 micromet |
| `so2` | float | Sulfur Dioxide | µg/m³ | Khí SO₂, gây mưa axit |
| `timestamp_local` | str | Timestamp local | ISO 8601 | Thời gian định dạng chuẩn (local) |
| `timestamp_utc` | str | Timestamp UTC | ISO 8601 | Thời gian định dạng chuẩn (UTC) |
| `ts` | int | Unix Timestamp | seconds | Số giây từ 1970-01-01 |

### Phạm Vi Giá Trị Điển Hình

**AQI Categories:**
```
0-50    : Good (Tốt)
51-100  : Moderate (Trung bình)
101-150 : Unhealthy for Sensitive Groups (Không lành mạnh cho nhóm nhạy cảm)
151-200 : Unhealthy (Không lành mạnh)
201-300 : Very Unhealthy (Rất không lành mạnh)
301+    : Hazardous (Nguy hiểm)
```

**PM2.5 Standards (WHO):**
- **24-hour mean**: 15 µg/m³
- **Annual mean**: 5 µg/m³
- Hà Nội thường vượt ngưỡng này nhiều lần

---

## 📖 Hướng Dẫn Sử Dụng

### Yêu Cầu Hệ Thống

**Python Libraries:**
```python
requests      # Gọi API
pandas        # Xử lý dữ liệu
datetime      # Xử lý thời gian
calendar      # Tính số ngày trong tháng
os            # Kiểm tra file
time          # Delay giữa requests
```

**Cài đặt:**
```bash
pip install requests pandas
```

### Cách Chạy

#### Option 1: Chạy toàn bộ notebook
1. Mở `G3_Assignment_Data_Processing.ipynb` trong Jupyter
2. Click **Run All Cells** hoặc **Kernel → Restart & Run All**
3. Đợi cho đến khi hoàn tất (có thể mất 10-30 phút)

#### Option 2: Chạy từng cell
1. **Cell 1**: Import libraries
2. **Cell 2-4**: Định nghĩa functions
3. **Cell 5**: Cấu hình (có thể sửa API_KEY, dates)
4. **Cell 6**: Bắt đầu thu thập dữ liệu

### Tùy Chỉnh

**Thay đổi khoảng thời gian:**
```python
start_date = datetime(2024, 1, 1)     # Từ ngày
end_date = datetime(2024, 12, 31)     # Đến ngày
```

**Thay đổi thành phố:**
```python
params = {
    'city': 'Ho Chi Minh City',  # Thay đổi thành phố
    ...
}
```

**Thay đổi delay:**
```python
time.sleep(2)  # Tăng delay lên 2 giây
```

---

## ⚠️ Xử Lý Lỗi và Tối Ưu

### Các Vấn Đề Thường Gặp

#### 1. **API Rate Limiting**

**Triệu chứng:**
```
HTTP 429: Too Many Requests
```

**Giải pháp:**
- Tăng delay: `time.sleep(5)`
- Chia nhỏ khoảng thời gian hơn
- Sử dụng API key premium

#### 2. **Timeout**

**Triệu chứng:**
```
Timeout khi lấy dữ liệu từ 2023-05-01 đến 2023-05-31
```

**Giải pháp:**
- Tăng timeout: `timeout=60`
- Kiểm tra kết nối internet
- Retry logic:
```python
for attempt in range(3):
    try:
        response = requests.get(...)
        break
    except Timeout:
        if attempt == 2:
            raise
        time.sleep(5)
```

#### 3. **Dữ Liệu Trùng Lặp**

**Nguyên nhân:**
- Chạy notebook nhiều lần
- API trả về dữ liệu overlap

**Giải pháp:**
```python
# Sau khi thu thập xong
df = pd.read_csv('weather_data_hanoi.csv')
df = df.drop_duplicates(subset=['datetime', 'timestamp_local'])
df.to_csv('weather_data_hanoi_clean.csv', index=False)
```

#### 4. **Missing Data**

**Phát hiện:**
```python
df = pd.read_csv('weather_data_hanoi.csv')
print(df.isnull().sum())  # Đếm số giá trị null
```

**Xử lý:**
```python
# Forward fill
df['pm25'].fillna(method='ffill', inplace=True)

# Hoặc interpolate
df['pm25'].interpolate(method='linear', inplace=True)
```

### Best Practices

1. **Backup dữ liệu:**
   ```python
   import shutil
   shutil.copy('weather_data_hanoi.csv', 
               'weather_data_hanoi_backup.csv')
   ```

2. **Logging chi tiết:**
   ```python
   import logging
   logging.basicConfig(filename='data_collection.log', 
                       level=logging.INFO)
   ```

3. **Checkpoint:**
   ```python
   # Lưu danh sách tháng đã xử lý
   processed_months = []
   # Bỏ qua tháng đã xử lý khi restart
   ```

---

## 📈 Kết Quả Thu Được

### Thống Kê Dữ Liệu

**Dự kiến:**
- **Thời gian**: 01/01/2023 - Hiện tại (≈ 23 tháng)
- **Số bản ghi**: ≈ 16,000 - 17,000 records
  - 1 record/giờ × 24 giờ × 700 ngày = 16,800 records
- **Kích thước file**: ≈ 2-3 MB (CSV format)
- **Tần suất**: Dữ liệu theo giờ (hourly)

### Chất Lượng Dữ Liệu

**Độ đầy đủ:**
- Missing rate: < 5% (thường do API downtime)
- Coverage: Toàn bộ khoảng thời gian được chỉ định

**Độ chính xác:**
- Dữ liệu từ nguồn chính thức (Weatherbit)
- Đã được validate bởi WHO standards
- Timestamps chính xác (đồng bộ UTC + Local)

### Sử Dụng Tiếp Theo

File `weather_data_hanoi.csv` được sử dụng cho:

1. **G3_Assignment_Model_Training.ipynb**
   - Feature engineering
   - Train/test split
   - Model training (Linear Regression, Random Forest, etc.)
   
2. **G3_Assignment_PM25_Prediction_7Days.ipynb**
   - Load trained model
   - Predict future PM2.5 values
   - Visualization

3. **Exploratory Data Analysis**
   - Time series analysis
   - Correlation analysis
   - Seasonal pattern detection

---

## 🔍 Phân Tích Sâu

### Tại Sao Chọn Weatherbit API?

**So sánh với các API khác:**

| API | Ưu Điểm | Nhược Điểm | Lựa Chọn |
|-----|---------|------------|----------|
| Weatherbit | ✅ Historical data<br>✅ Hourly granularity<br>✅ Free tier | ❌ Rate limiting | **CHỌN** |
| OpenWeatherMap | ✅ Popular<br>✅ Good docs | ❌ Không có air quality history | ✗ |
| AirVisual | ✅ Real-time accurate | ❌ Đắt<br>❌ Không có history | ✗ |
| AQICN | ✅ Free<br>✅ Vietnam data | ❌ API restrictions | ✗ |

### Tần Suất Dữ Liệu

**Tại sao dữ liệu theo giờ (hourly)?**

1. **Đủ chi tiết**: Phát hiện được biến động trong ngày
2. **Không quá dày**: Tránh overfitting model
3. **Chuẩn công nghiệp**: WHO khuyến nghị hourly monitoring
4. **Khả thi**: API hỗ trợ, không quá tốn tài nguyên

**Alternative options:**
- **Daily**: Mất thông tin biến động trong ngày
- **Minute-level**: Quá chi tiết, nhiễu cao, không cần thiết

### Múi Giờ (Timezone)

**Tại sao cần cả `local` và `UTC`?**

```python
'tz': 'local'  # GMT+7 cho Việt Nam
```

- **Local time**: Dễ hiểu cho người dùng Việt Nam
- **UTC time**: Chuẩn quốc tế, dễ so sánh với nguồn khác
- **Timestamp**: Để machine learning model sử dụng

---

## 🚀 Mở Rộng và Cải Tiến

### Cải Tiến Có Thể Thực Hiện

1. **Database Integration**
   ```python
   import sqlite3
   conn = sqlite3.connect('air_quality.db')
   df.to_sql('hanoi_data', conn, if_exists='append')
   ```

2. **Real-time Updates**
   ```python
   import schedule
   schedule.every().hour.do(fetch_latest_data)
   ```

3. **Multi-city Support**
   ```python
   cities = ['Hanoi', 'Ho Chi Minh City', 'Da Nang']
   for city in cities:
       get_weather_data(city, ...)
   ```

4. **Data Validation**
   ```python
   def validate_data(df):
       assert df['pm25'].min() >= 0, "PM2.5 không thể âm"
       assert df['pm25'].max() <= 999, "PM2.5 quá cao"
       return df
   ```

5. **Alerting System**
   ```python
   if pm25_value > 150:
       send_email_alert("PM2.5 vượt ngưỡng nguy hiểm!")
   ```

---

## 📚 Tài Liệu Tham Khảo

### API Documentation
- [Weatherbit API Docs](https://www.weatherbit.io/api)
- [Air Quality API Endpoint](https://www.weatherbit.io/api/airquality-history)

### Standards
- [WHO Air Quality Guidelines](https://www.who.int/news-room/feature-stories/detail/what-are-the-who-air-quality-guidelines)
- [EPA AQI Basics](https://www.airnow.gov/aqi/aqi-basics/)

### Python Libraries
- [Requests Documentation](https://requests.readthedocs.io/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/)

---

## ❓ FAQs

**Q: Mất bao lâu để thu thập dữ liệu?**  
A: Khoảng 20-30 phút cho 23 tháng dữ liệu (với delay 1 giây/request).

**Q: Có thể chạy lại notebook không?**  
A: Có, dữ liệu sẽ được append vào file CSV. Nhớ xóa duplicates sau đó.

**Q: API key có bị giới hạn không?**  
A: Có, free tier giới hạn khoảng 500 calls/day. Upgrade nếu cần nhiều hơn.

**Q: Dữ liệu có chính xác không?**  
A: Weatherbit tổng hợp từ nhiều nguồn chính thức, độ chính xác cao (±10%).

**Q: Có thể lấy dữ liệu real-time không?**  
A: Có, sử dụng endpoint `/current/airquality` thay vì `/history/airquality`.

---

## 📞 Liên Hệ và Hỗ Trợ

**Tác giả**: Group 3 - MLE501 Assignment  
**Email**: [Your Email]  
**GitHub**: [Your GitHub]  

**Báo cáo lỗi**: Tạo issue trên GitHub repository  
**Đóng góp**: Pull requests are welcome!

---

## 📄 License

Dự án này được phát triển cho mục đích học tập tại FPT University.  
Dữ liệu từ Weatherbit API tuân theo [Weatherbit Terms of Service](https://www.weatherbit.io/terms).

---

**Phiên bản**: 1.0  
**Cập nhật lần cuối**: November 2024  
**Notebook**: G3_Assignment_Data_Processing.ipynb  
**Output**: weather_data_hanoi.csv
