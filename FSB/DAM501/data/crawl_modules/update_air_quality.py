"""
Script để cập nhật dữ liệu chất lượng không khí Hà Nội từ Weatherbit API
Lấy dữ liệu từ 2025-09-30:17 đến hiện tại
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os

# Cấu hình
API_KEY = "3bc5b17af28142a3822c00233ee708dd"
LAT = 21.0285  # Hà Nội
LON = 105.8542
DATA_FILE = "../data_file/hanoi_air_quality_history.csv"

# Bắt đầu từ ngày 2025-09-30 00:00
start_date = datetime(2025, 9, 30, 0)
print(f"📅 Bắt đầu từ: {start_date.strftime('%Y-%m-%d %H:00')}")

# Đọc dữ liệu hiện tại
existing_df = pd.read_csv(DATA_FILE)
end_date = datetime.now()

print(f"🔄 Cập nhật từ {start_date.strftime('%Y-%m-%d %H:00')} đến {end_date.strftime('%Y-%m-%d %H:00')}")

# Weatherbit API giới hạn 30 ngày mỗi request
def get_air_quality_data(start, end):
    """
    Lấy dữ liệu air quality từ Weatherbit API
    """
    start_str = start.strftime("%Y-%m-%d:%H")
    end_str = end.strftime("%Y-%m-%d:%H")
    
    url = "https://api.weatherbit.io/v2.0/history/airquality"
    params = {
        'lat': LAT,
        'lon': LON,
        'start_date': start_str,
        'end_date': end_str,
        'key': API_KEY,
        'tz': 'local'
    }
    
    print(f"   🌐 Fetching: {start_str} → {end_str}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            return data['data']
        else:
            print(f"   ⚠️  Không có dữ liệu cho khoảng thời gian này")
            return []
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Lỗi API: {e}")
        return []

# Chia thành các chunk 30 ngày
all_records = []
current_start = start_date

while current_start < end_date:
    current_end = min(current_start + timedelta(days=30), end_date)
    
    # Lấy dữ liệu
    records = get_air_quality_data(current_start, current_end)
    
    if records:
        all_records.extend(records)
        print(f"   ✅ Lấy được {len(records)} records")
    
    # Di chuyển đến chunk tiếp theo
    current_start = current_end + timedelta(hours=1)
    
    # Tránh rate limit
    time.sleep(1)

# Xử lý dữ liệu
if all_records:
    print(f"\n📊 Tổng cộng: {len(all_records)} records")
    
    # Chuyển đổi sang DataFrame
    new_data = []
    for record in all_records:
        # Parse timestamp
        timestamp = record.get('timestamp_local', record.get('timestamp_utc', ''))
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        datetime_str = dt.strftime("%Y-%m-%d:%H")
        
        new_data.append({
            'datetime': datetime_str,
            'aqi': record.get('aqi', 0),
            'pm25': record.get('pm25', 0.0),
            'pm10': record.get('pm10', 0.0),
            'o3': record.get('o3', 0.0),
            'so2': record.get('so2', 0.0),
            'no2': record.get('no2', 0.0),
            'co': record.get('co', 0.0)
        })
    
    new_df = pd.DataFrame(new_data)
    
    # Loại bỏ duplicate (nếu có)
    new_df = new_df.drop_duplicates(subset=['datetime'], keep='first')
    
    # Sắp xếp theo thời gian giảm dần (mới nhất ở đầu)
    new_df = new_df.sort_values('datetime', ascending=False)
    
    print(f"📝 Dữ liệu mới sau xử lý: {len(new_df)} records")
    
    # Gộp với dữ liệu cũ
    combined_df = pd.concat([new_df, existing_df], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=['datetime'], keep='first')
    combined_df = combined_df.sort_values('datetime', ascending=False)
    
    # Lưu file
    combined_df.to_csv(DATA_FILE, index=False)
    
    print(f"\n✅ Đã cập nhật file: {DATA_FILE}")
    print(f"📈 Tổng records: {len(combined_df)}")
    print(f"🆕 Thêm mới: {len(new_df)} records")
    print(f"\n📅 Dữ liệu mới nhất: {combined_df['datetime'].iloc[0]}")
    print(f"📅 Dữ liệu cũ nhất: {combined_df['datetime'].iloc[-1]}")
    
    # Hiển thị mẫu
    print("\n📋 5 records mới nhất:")
    print(combined_df.head())
    
else:
    print("\n⚠️  Không có dữ liệu mới để cập nhật")
