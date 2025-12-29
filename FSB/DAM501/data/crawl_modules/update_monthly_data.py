"""
Script cập nhật dữ liệu Air Quality và Weather theo THÁNG
Lấy dữ liệu từ 2025-09-30 (Air Quality) và 2025-10-30 (Weather) đến hiện tại
"""

import requests
import pandas as pd
from datetime import datetime
from calendar import monthrange
import time
import os

# Cấu hình
API_KEY = "3bc5b17af28142a3822c00233ee708dd"
LAT = 21.0285  # Hà Nội
LON = 105.8542

AIR_QUALITY_FILE = "../data_file/hanoi_air_quality_history.csv"
WEATHER_FILE = "../data_file/hanoi_weather_history.csv"

def get_air_quality_data(start_date, end_date):
    """Lấy dữ liệu Air Quality History"""
    url = "https://api.weatherbit.io/v2.0/history/airquality"
    params = {
        'lat': LAT,
        'lon': LON,
        'start_date': start_date,
        'end_date': end_date,
        'tz': 'local',
        'key': API_KEY
    }
    
    try:
        print(f"   🌐 Air Quality: {start_date} → {end_date}")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        records = data.get('data', [])
        
        if records:
            df = pd.DataFrame(records)
            # Chọn các cột cần thiết
            air_cols = ['datetime', 'aqi', 'pm25', 'pm10', 'o3', 'so2', 'no2', 'co']
            existing_cols = [col for col in air_cols if col in df.columns]
            df = df[existing_cols]
            
            # Convert datetime format từ "2025-09-30:17" sang "2025-09-30:17"
            if 'datetime' in df.columns:
                # Giữ nguyên format YYYY-MM-DD:HH
                pass
            
            print(f"      ✅ Lấy được {len(df)} records")
            return df
        else:
            print(f"      ⚠️  Không có dữ liệu")
            return None
            
    except Exception as e:
        print(f"      ❌ Lỗi: {e}")
        return None

def get_weather_data(start_date, end_date):
    """Lấy dữ liệu Weather History"""
    url = "https://api.weatherbit.io/v2.0/history/hourly"
    params = {
        'lat': LAT,
        'lon': LON,
        'start_date': start_date,
        'end_date': end_date,
        'tz': 'local',
        'key': API_KEY
    }
    
    try:
        print(f"   🌐 Weather: {start_date} → {end_date}")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        records = data.get('data', [])
        
        if records:
            df = pd.DataFrame(records)
            # Chọn các cột cần thiết
            weather_cols = ['datetime', 'temp', 'app_temp', 'rh', 'wind_spd', 'wind_dir', 
                           'pres', 'vis', 'clouds', 'precip', 'uv', 'dewpt']
            existing_cols = [col for col in weather_cols if col in df.columns]
            df = df[existing_cols]
            
            print(f"      ✅ Lấy được {len(df)} records")
            return df
        else:
            print(f"      ⚠️  Không có dữ liệu")
            return None
            
    except Exception as e:
        print(f"      ❌ Lỗi: {e}")
        return None

def get_months_between_dates(start_date, end_date):
    """Lấy danh sách các khoảng thời gian theo tháng"""
    months = []
    start_year, start_month = start_date.year, start_date.month
    end_year, end_month = end_date.year, end_date.month

    while start_year < end_year or (start_year == end_year and start_month <= end_month):
        # Ngày bắt đầu tháng
        month_start = datetime(start_year, start_month, 1)
        
        # Ngày cuối tháng
        _, last_day = monthrange(start_year, start_month)
        month_end = datetime(start_year, start_month, last_day)
        
        # Không vượt quá end_date
        if month_end > end_date:
            month_end = end_date

        months.append((
            month_start.strftime('%Y-%m-%d'), 
            month_end.strftime('%Y-%m-%d')
        ))

        # Sang tháng tiếp theo
        if start_month == 12:
            start_month = 1
            start_year += 1
        else:
            start_month += 1

    return months

def update_air_quality():
    """Cập nhật Air Quality từ 2025-09-30"""
    print("\n" + "="*80)
    print("📊 CẬP NHẬT AIR QUALITY DATA")
    print("="*80)
    
    # Bắt đầu từ 2025-09-30
    start_date = datetime(2025, 9, 30)
    end_date = datetime.now()
    
    print(f"Từ: {start_date.strftime('%Y-%m-%d')}")
    print(f"Đến: {end_date.strftime('%Y-%m-%d')}")
    
    # Lấy danh sách tháng
    months = get_months_between_dates(start_date, end_date)
    print(f"Tổng số tháng: {len(months)}")
    
    all_data = []
    
    for i, (month_start, month_end) in enumerate(months, 1):
        print(f"\n📅 Tháng {i}/{len(months)}: {month_start} → {month_end}")
        
        df = get_air_quality_data(month_start, month_end)
        
        if df is not None and not df.empty:
            all_data.append(df)
        
        # Delay để tránh rate limit
        if i < len(months):
            time.sleep(1)
    
    # Gộp tất cả dữ liệu
    if all_data:
        new_df = pd.concat(all_data, ignore_index=True)
        new_df = new_df.drop_duplicates(subset=['datetime'], keep='first')
        new_df = new_df.sort_values('datetime', ascending=False)
        
        print(f"\n📊 Tổng dữ liệu mới: {len(new_df)} records")
        
        # Đọc dữ liệu cũ
        existing_df = pd.read_csv(AIR_QUALITY_FILE)
        
        # Gộp với dữ liệu cũ
        combined_df = pd.concat([new_df, existing_df], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['datetime'], keep='first')
        combined_df = combined_df.sort_values('datetime', ascending=False)
        
        # Lưu file
        combined_df.to_csv(AIR_QUALITY_FILE, index=False)
        
        print(f"✅ Đã cập nhật {AIR_QUALITY_FILE}")
        print(f"   📈 Tổng records: {len(combined_df)}")
        print(f"   🆕 Thêm mới: {len(new_df)} records")
        print(f"   📅 Mới nhất: {combined_df['datetime'].iloc[0]}")
        
        return True
    else:
        print("\n⚠️  Không có dữ liệu mới")
        return False

def update_weather():
    """Cập nhật Weather từ 2025-10-30"""
    print("\n" + "="*80)
    print("🌤️  CẬP NHẬT WEATHER DATA")
    print("="*80)
    
    # Bắt đầu từ 2025-10-30
    start_date = datetime(2025, 10, 30)
    end_date = datetime.now()
    
    print(f"Từ: {start_date.strftime('%Y-%m-%d')}")
    print(f"Đến: {end_date.strftime('%Y-%m-%d')}")
    
    # Lấy danh sách tháng
    months = get_months_between_dates(start_date, end_date)
    print(f"Tổng số tháng: {len(months)}")
    
    all_data = []
    
    for i, (month_start, month_end) in enumerate(months, 1):
        print(f"\n📅 Tháng {i}/{len(months)}: {month_start} → {month_end}")
        
        df = get_weather_data(month_start, month_end)
        
        if df is not None and not df.empty:
            all_data.append(df)
        
        # Delay để tránh rate limit
        if i < len(months):
            time.sleep(1)
    
    # Gộp tất cả dữ liệu
    if all_data:
        new_df = pd.concat(all_data, ignore_index=True)
        new_df = new_df.drop_duplicates(subset=['datetime'], keep='first')
        new_df = new_df.sort_values('datetime', ascending=False)
        
        print(f"\n📊 Tổng dữ liệu mới: {len(new_df)} records")
        
        # Đọc dữ liệu cũ
        existing_df = pd.read_csv(WEATHER_FILE)
        
        # Gộp với dữ liệu cũ
        combined_df = pd.concat([new_df, existing_df], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['datetime'], keep='first')
        combined_df = combined_df.sort_values('datetime', ascending=False)
        
        # Lưu file
        combined_df.to_csv(WEATHER_FILE, index=False)
        
        print(f"✅ Đã cập nhật {WEATHER_FILE}")
        print(f"   📈 Tổng records: {len(combined_df)}")
        print(f"   🆕 Thêm mới: {len(new_df)} records")
        print(f"   📅 Mới nhất: {combined_df['datetime'].iloc[0]}")
        
        return True
    else:
        print("\n⚠️  Không có dữ liệu mới")
        return False

if __name__ == "__main__":
    print("="*80)
    print("🚀 CẬP NHẬT DỮ LIỆU TỪ WEATHERBIT API (THEO THÁNG)")
    print("="*80)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Cập nhật cả 2 loại dữ liệu
    air_updated = update_air_quality()
    weather_updated = update_weather()
    
    print("\n" + "="*80)
    if air_updated or weather_updated:
        print("✨ CẬP NHẬT THÀNH CÔNG!")
    else:
        print("ℹ️  Không có dữ liệu mới để cập nhật")
    print("="*80)
