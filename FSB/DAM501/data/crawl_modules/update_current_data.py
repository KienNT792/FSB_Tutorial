"""
Script cập nhật dữ liệu Air Quality và Weather HIỆN TẠI từ Weatherbit API (Free tier)
Vì Historical API cần trả phí, script này sẽ lấy dữ liệu current và append vào file
Nên chạy script này mỗi giờ bằng cron job để thu thập dữ liệu theo thời gian
"""

import requests
import pandas as pd
from datetime import datetime
import os

# Cấu hình
API_KEY = "3bc5b17af28142a3822c00233ee708dd"
LAT = 21.0285  # Hà Nội
LON = 105.8542

AIR_QUALITY_FILE = "../data_file/hanoi_air_quality_history.csv"
WEATHER_FILE = "../data_file/hanoi_weather_history.csv"

def get_current_air_quality():
    """Lấy dữ liệu Air Quality hiện tại (Free API)"""
    url = "https://api.weatherbit.io/v2.0/current/airquality"
    params = {
        'lat': LAT,
        'lon': LON,
        'key': API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            record = data['data'][0]
            
            # Parse timestamp
            timestamp = record.get('timestamp_local', record.get('ob_time', ''))
            if timestamp:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                dt = datetime.now()
            
            datetime_str = dt.strftime("%Y-%m-%d:%H")
            
            return {
                'datetime': datetime_str,
                'aqi': record.get('aqi', 0),
                'pm25': record.get('pm25', 0.0),
                'pm10': record.get('pm10', 0.0),
                'o3': record.get('o3', 0.0),
                'so2': record.get('so2', 0.0),
                'no2': record.get('no2', 0.0),
                'co': record.get('co', 0.0)
            }
        return None
    except Exception as e:
        print(f"❌ Lỗi Air Quality API: {e}")
        return None

def get_current_weather():
    """Lấy dữ liệu Weather hiện tại (Free API)"""
    url = "https://api.weatherbit.io/v2.0/current"
    params = {
        'lat': LAT,
        'lon': LON,
        'key': API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            record = data['data'][0]
            
            # Parse timestamp
            timestamp = record.get('ob_time', '')
            if timestamp:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                dt = datetime.now()
            
            datetime_str = dt.strftime("%Y-%m-%d:%H")
            
            return {
                'datetime': datetime_str,
                'temp': record.get('temp', 0.0),
                'app_temp': record.get('app_temp', 0.0),
                'rh': record.get('rh', 0),
                'wind_spd': record.get('wind_spd', 0.0),
                'wind_dir': record.get('wind_dir', 0),
                'pres': record.get('pres', 0),
                'vis': record.get('vis', 0.0),
                'clouds': record.get('clouds', 0),
                'precip': record.get('precip', 0.0),
                'uv': record.get('uv', 0.0),
                'dewpt': record.get('dewpt', 0.0)
            }
        return None
    except Exception as e:
        print(f"❌ Lỗi Weather API: {e}")
        return None

def update_air_quality():
    """Cập nhật Air Quality data"""
    print("🌍 Đang lấy dữ liệu Air Quality...")
    
    new_record = get_current_air_quality()
    
    if new_record:
        # Đọc file hiện tại
        existing_df = pd.read_csv(AIR_QUALITY_FILE)
        
        # Kiểm tra xem đã có data cho giờ này chưa
        if new_record['datetime'] in existing_df['datetime'].values:
            print(f"⚠️  Đã có dữ liệu cho {new_record['datetime']}, bỏ qua")
            return False
        
        # Thêm record mới
        new_df = pd.DataFrame([new_record])
        combined_df = pd.concat([new_df, existing_df], ignore_index=True)
        combined_df = combined_df.sort_values('datetime', ascending=False)
        
        # Lưu file
        combined_df.to_csv(AIR_QUALITY_FILE, index=False)
        
        print(f"✅ Đã cập nhật Air Quality: {new_record['datetime']}")
        print(f"   AQI: {new_record['aqi']}, PM2.5: {new_record['pm25']}")
        print(f"📊 Tổng records: {len(combined_df)}")
        return True
    
    return False

def update_weather():
    """Cập nhật Weather data"""
    print("\n🌤️  Đang lấy dữ liệu Weather...")
    
    new_record = get_current_weather()
    
    if new_record:
        # Đọc file hiện tại
        existing_df = pd.read_csv(WEATHER_FILE)
        
        # Kiểm tra xem đã có data cho giờ này chưa
        if new_record['datetime'] in existing_df['datetime'].values:
            print(f"⚠️  Đã có dữ liệu cho {new_record['datetime']}, bỏ qua")
            return False
        
        # Thêm record mới
        new_df = pd.DataFrame([new_record])
        combined_df = pd.concat([new_df, existing_df], ignore_index=True)
        combined_df = combined_df.sort_values('datetime', ascending=False)
        
        # Lưu file
        combined_df.to_csv(WEATHER_FILE, index=False)
        
        print(f"✅ Đã cập nhật Weather: {new_record['datetime']}")
        print(f"   Temp: {new_record['temp']}°C, RH: {new_record['rh']}%")
        print(f"📊 Tổng records: {len(combined_df)}")
        return True
    
    return False

if __name__ == "__main__":
    print("=" * 80)
    print("📡 CẬP NHẬT DỮ LIỆU HIỆN TẠI TỪ WEATHERBIT API")
    print("=" * 80)
    print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Cập nhật cả 2 loại dữ liệu
    air_updated = update_air_quality()
    weather_updated = update_weather()
    
    print("\n" + "=" * 80)
    if air_updated or weather_updated:
        print("✨ CẬP NHẬT THÀNH CÔNG!")
    else:
        print("ℹ️  Không có dữ liệu mới")
    print("=" * 80)
    
    print("\n💡 LƯU Ý:")
    print("   • Script này chỉ lấy dữ liệu HIỆN TẠI (Free API)")
    print("   • Historical API cần gói trả phí")
    print("   • Nên setup cron job chạy script này mỗi giờ để thu thập dữ liệu:")
    print("     0 * * * * cd /path/to/crawl_modules && python update_current_data.py")
