#!/usr/bin/env python3
"""
Script tự động cập nhật dữ liệu và dự đoán PM2.5 cho 1 giờ tới
Sử dụng mô hình CatBoost đã được huấn luyện
"""

import pandas as pd
import numpy as np
import joblib
import requests
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Cấu hình
API_KEY = '3bc5b17af28142a3822c00233ee708dd'
CITY = 'Hanoi'
LAT = 21.0285
LON = 105.8542

DATA_PATH = 'data/data_file/'
MODEL_PATH = '../notebook/output/'
MODEL_FILE = 'xgboost_model_1h.pkl'  # Sử dụng XGBoost thay vì CatBoost

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def fetch_current_data():
    """Lấy dữ liệu hiện tại từ Weatherbit API"""
    print_header("BƯỚC 1: CẬP NHẬT DỮ LIỆU MỚI NHẤT")
    
    # Fetch current air quality
    print_info("Đang lấy dữ liệu chất lượng không khí...")
    air_url = f'https://api.weatherbit.io/v2.0/current/airquality?city={CITY}&key={API_KEY}'
    try:
        air_response = requests.get(air_url, timeout=10)
        air_response.raise_for_status()
        air_data = air_response.json()['data'][0]
        print_success(f"Lấy dữ liệu không khí thành công - {air_data['datetime']}")
    except Exception as e:
        print_error(f"Lỗi khi lấy dữ liệu không khí: {e}")
        return None
    
    # Fetch current weather
    print_info("Đang lấy dữ liệu thời tiết...")
    weather_url = f'https://api.weatherbit.io/v2.0/current?city={CITY}&key={API_KEY}'
    try:
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()['data'][0]
        print_success(f"Lấy dữ liệu thời tiết thành công - {weather_data['datetime']}")
    except Exception as e:
        print_error(f"Lỗi khi lấy dữ liệu thời tiết: {e}")
        return None
    
    # Combine data
    current_datetime = pd.to_datetime(air_data['datetime'], format='%Y-%m-%d:%H')
    
    current_record = {
        'datetime': current_datetime,
        'pm25': air_data.get('pm25', np.nan),
        'pm10': air_data.get('pm10', np.nan),
        'o3': air_data.get('o3', np.nan),
        'so2': air_data.get('so2', np.nan),
        'no2': air_data.get('no2', np.nan),
        'co': air_data.get('co', np.nan),
        'temp': weather_data.get('temp', np.nan),
        'rh': weather_data.get('rh', np.nan),
        'wind_spd': weather_data.get('wind_spd', np.nan),
        'wind_dir': weather_data.get('wind_dir', np.nan),
        'pres': weather_data.get('pres', np.nan),
        'vis': weather_data.get('vis', np.nan),
        'clouds': weather_data.get('clouds', np.nan),
        'precip': weather_data.get('precip', np.nan),
    }
    
    return current_record

def load_historical_data():
    """Load dữ liệu lịch sử từ CSV files"""
    print_header("BƯỚC 2: LOAD DỮ LIỆU LỊCH SỬ")
    
    try:
        print_info("Đang đọc dữ liệu không khí...")
        air = pd.read_csv(f'{DATA_PATH}hanoi_air_quality_history.csv')
        air['datetime'] = pd.to_datetime(air['datetime'], format='%Y-%m-%d:%H')
        print_success(f"Đã đọc {len(air):,} bản ghi không khí")
        
        print_info("Đang đọc dữ liệu thời tiết...")
        weather = pd.read_csv(f'{DATA_PATH}hanoi_weather_history.csv')
        weather['datetime'] = pd.to_datetime(weather['datetime'], format='%Y-%m-%d:%H')
        print_success(f"Đã đọc {len(weather):,} bản ghi thời tiết")
        
        print_info("Đang đọc dữ liệu ngày lễ...")
        holidays = pd.read_csv(f'{DATA_PATH}hanoi_holidays_aligned.csv')
        holidays['datetime'] = pd.to_datetime(holidays['datetime'])
        print_success(f"Đã đọc {len(holidays):,} bản ghi ngày lễ")
        
        print_info("Đang đọc dữ liệu giao thông...")
        traffic = pd.read_csv(f'{DATA_PATH}hanoi_traffic_proxy.csv')
        traffic['datetime'] = pd.to_datetime(traffic['datetime'])
        print_success(f"Đã đọc {len(traffic):,} bản ghi giao thông")
        
        # Merge datasets - Sử dụng LEFT JOIN để giữ tất cả air quality data
        print_info("Đang merge dữ liệu...")
        df = pd.merge(air, weather, on='datetime', how='left')
        df = pd.merge(df, holidays[['datetime', 'is_holiday', 'holiday_name']], 
                     on='datetime', how='left')
        df = pd.merge(df, traffic[['datetime', 'congestion_index', 'congestion_noise']], 
                     on='datetime', how='left')
        
        # Sort by datetime first
        df = df.sort_values('datetime').reset_index(drop=True)
        
        # Fill missing weather data với forward fill (sử dụng giá trị gần nhất)
        weather_cols = ['temp', 'rh', 'wind_spd', 'wind_dir', 'pres', 'vis', 'clouds', 'precip']
        for col in weather_cols:
            if col in df.columns:
                df[col] = df[col].fillna(method='ffill')
        
        # Fill missing values
        df['is_holiday'] = df['is_holiday'].fillna(0).astype(int)
        df['holiday_name'] = df['holiday_name'].fillna('')
        df['congestion_index'] = df['congestion_index'].fillna(method='ffill').fillna(df['congestion_index'].median())
        df['congestion_noise'] = df['congestion_noise'].fillna(0)
        
        print_success(f"Merge thành công: {len(df):,} bản ghi từ {df['datetime'].min()} đến {df['datetime'].max()}")
        
        return df
    
    except Exception as e:
        print_error(f"Lỗi khi load dữ liệu: {e}")
        return None

def engineer_features(df):
    """Tạo các đặc trưng giống như trong notebook"""
    print_header("BƯỚC 3: TẠO ĐẶC TRƯNG (FEATURE ENGINEERING)")
    
    df = df.copy()
    
    print_info("Tạo time features...")
    # Time features
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['month'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    
    # Cyclical encoding
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    
    # Wind direction
    if 'wind_dir' in df.columns:
        df['wind_dir'] = df['wind_dir'] % 360
        df['wind_dir_rad'] = np.deg2rad(df['wind_dir'])
        df['wind_dir_sin'] = np.sin(df['wind_dir_rad'])
        df['wind_dir_cos'] = np.cos(df['wind_dir_rad'])
        df.drop(columns=['wind_dir', 'wind_dir_rad'], inplace=True)
    
    print_info("Tạo lag features...")
    # Lag features
    lags = [1, 3, 6, 12, 24, 48, 72]
    for lag in lags:
        df[f'pm25_lag_{lag}'] = df['pm25'].shift(lag)
        df[f'temp_lag_{lag}'] = df['temp'].shift(lag)
        df[f'wind_spd_lag_{lag}'] = df['wind_spd'].shift(lag)
        if 'congestion_index' in df.columns:
            df[f'traffic_lag_{lag}'] = df['congestion_index'].shift(lag)
    
    print_info("Tạo rolling statistics...")
    # Rolling statistics
    windows = [6, 12, 24, 48]
    for win in windows:
        df[f'pm25_roll_mean_{win}'] = df['pm25'].rolling(win).mean()
        df[f'pm25_roll_std_{win}'] = df['pm25'].rolling(win).std()
        df[f'pm25_roll_min_{win}'] = df['pm25'].rolling(win).min()
        df[f'pm25_roll_max_{win}'] = df['pm25'].rolling(win).max()
    
    print_info("Tạo difference features...")
    # Difference features
    df['pm25_diff_1h'] = df['pm25'].diff(1)
    df['pm25_diff_24h'] = df['pm25'].diff(24)
    df['temp_diff_1h'] = df['temp'].diff(1)
    
    print_info("Tạo categorical features...")
    # Categorical features
    df['is_peak_hour'] = df['hour'].apply(lambda x: 1 if x in [7, 8, 9, 17, 18, 19] else 0)
    df['is_night'] = df['hour'].apply(lambda x: 1 if x >= 22 or x <= 6 else 0)
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    # Traffic features
    if 'congestion_index' in df.columns:
        df['high_traffic'] = (df['congestion_index'] > df['congestion_index'].quantile(0.75)).astype(int)
        df['low_traffic'] = (df['congestion_index'] < df['congestion_index'].quantile(0.25)).astype(int)
    
    print_info("Tạo interaction features...")
    # Interaction features
    df['temp_x_rh'] = df['temp'] * df['rh']
    df['wind_spd_x_temp'] = df['wind_spd'] * df['temp']
    
    if 'congestion_index' in df.columns:
        df['traffic_x_hour'] = df['congestion_index'] * df['hour']
        df['traffic_x_holiday'] = df['congestion_index'] * df.get('is_holiday', 0)
        df['pm25_x_traffic'] = df['pm25'] * df['congestion_index']
    
    print_success(f"Đã tạo {df.shape[1]} features")
    
    return df

def predict_next_hour(df):
    """Dự đoán PM2.5 cho 1 giờ tới"""
    print_header("BƯỚC 4: DỰ ĐOÁN PM2.5 CHO 1 GIỜ TỚI")
    
    # Load model
    model_path = f'{MODEL_PATH}{MODEL_FILE}'
    if not os.path.exists(model_path):
        print_error(f"Không tìm thấy model: {model_path}")
        return None
    
    print_info(f"Đang load model từ {model_path}...")
    try:
        model = joblib.load(model_path)
        print_success("Load model thành công!")
    except Exception as e:
        print_error(f"Lỗi khi load model: {e}")
        return None
    
    # Prepare features
    exclude_cols = ['datetime', 'pm25', 'target', 'holiday_name']
    features = [c for c in df.columns if c not in exclude_cols]
    
    # Get latest record (với đầy đủ features)
    df_valid = df.dropna().reset_index(drop=True)
    if len(df_valid) == 0:
        print_error("Không có dữ liệu hợp lệ sau khi loại bỏ NaN!")
        return None
    
    latest_record = df_valid.iloc[-1:][features]
    current_pm25 = df_valid.iloc[-1]['pm25']
    current_time = df_valid.iloc[-1]['datetime']
    
    print_info(f"Dữ liệu hiện tại:")
    print(f"   📅 Thời gian: {current_time}")
    print(f"   🌫️  PM2.5 hiện tại: {current_pm25:.2f} μg/m³")
    
    # Make prediction
    print_info("Đang thực hiện dự đoán...")
    try:
        prediction = model.predict(latest_record)[0]
        forecast_time = current_time + timedelta(hours=1)
        
        print_success("Dự đoán thành công!")
        
        return {
            'current_time': current_time,
            'forecast_time': forecast_time,
            'current_pm25': current_pm25,
            'predicted_pm25': prediction,
            'change': prediction - current_pm25,
            'change_pct': (prediction - current_pm25) / current_pm25 * 100
        }
    
    except Exception as e:
        print_error(f"Lỗi khi dự đoán: {e}")
        return None

def get_aqi_level(pm25):
    """Xác định mức độ AQI từ PM2.5"""
    if pm25 <= 12:
        return "TỐT", Colors.GREEN
    elif pm25 <= 35.4:
        return "TRUNG BÌNH", Colors.BLUE
    elif pm25 <= 55.4:
        return "KÉM", Colors.YELLOW
    elif pm25 <= 150.4:
        return "XẤU", Colors.RED
    elif pm25 <= 250.4:
        return "RẤT XẤU", Colors.RED
    else:
        return "NGUY HIỂM", Colors.RED

def display_results(result):
    """Hiển thị kết quả dự đoán"""
    print_header("KẾT QUẢ DỰ ĐOÁN PM2.5 - 1 GIỜ TỚI")
    
    # Current status
    current_level, current_color = get_aqi_level(result['current_pm25'])
    print(f"{Colors.BOLD}📍 HIỆN TẠI ({result['current_time'].strftime('%Y-%m-%d %H:%M')}){Colors.END}")
    print(f"   PM2.5: {current_color}{result['current_pm25']:.2f} μg/m³{Colors.END}")
    print(f"   Mức độ: {current_color}{current_level}{Colors.END}")
    
    print()
    
    # Forecast
    forecast_level, forecast_color = get_aqi_level(result['predicted_pm25'])
    print(f"{Colors.BOLD}🔮 DỰ ĐOÁN ({result['forecast_time'].strftime('%Y-%m-%d %H:%M')}){Colors.END}")
    print(f"   PM2.5: {forecast_color}{result['predicted_pm25']:.2f} μg/m³{Colors.END}")
    print(f"   Mức độ: {forecast_color}{forecast_level}{Colors.END}")
    
    print()
    
    # Change
    change_symbol = "📈" if result['change'] > 0 else "📉" if result['change'] < 0 else "➡️"
    change_color = Colors.RED if result['change'] > 0 else Colors.GREEN if result['change'] < 0 else Colors.BLUE
    
    print(f"{Colors.BOLD}📊 THAY ĐỔI{Colors.END}")
    print(f"   {change_symbol} {change_color}{result['change']:+.2f} μg/m³ ({result['change_pct']:+.1f}%){Colors.END}")
    
    print()
    
    # Recommendations
    print(f"{Colors.BOLD}💡 KHUYẾN NGHỊ{Colors.END}")
    if result['predicted_pm25'] > 55.4:
        print(f"   {Colors.RED}⚠️  Chất lượng không khí XẤU - Hạn chế ra ngoài{Colors.END}")
        print(f"   {Colors.RED}⚠️  Đeo khẩu trang khi ra đường{Colors.END}")
    elif result['predicted_pm25'] > 35.4:
        print(f"   {Colors.YELLOW}⚠️  Chất lượng không khí KÉM - Cẩn thận khi ra ngoài{Colors.END}")
    else:
        print(f"   {Colors.GREEN}✓ Chất lượng không khí ở mức chấp nhận được{Colors.END}")
    
    print()
    
    # Model info
    print(f"{Colors.BOLD}ℹ️  THÔNG TIN MÔ HÌNH{Colors.END}")
    print(f"   Model: XGBoost Regressor")
    print(f"   Horizon: 1 giờ")
    print(f"   R² Score: ~0.754 (từ kết quả huấn luyện)")
    print(f"   MAE: ~8.71 μg/m³")

def main():
    """Main function"""
    print_header("🌫️  HỆ THỐNG DỰ BÁO PM2.5 HÀ NỘI - 1 GIỜ TỚI")
    print(f"{Colors.BOLD}Thời gian chạy: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    
    # Step 1: Fetch current data (optional - comment out if API limit)
    # current_data = fetch_current_data()
    # if current_data is None:
    #     print_warning("Không thể lấy dữ liệu real-time, sử dụng dữ liệu lịch sử")
    
    # Step 2: Load historical data
    df = load_historical_data()
    if df is None:
        print_error("Không thể load dữ liệu lịch sử!")
        return
    
    # Step 3: Feature engineering
    df_feat = engineer_features(df)
    
    # Step 4: Make prediction
    result = predict_next_hour(df_feat)
    if result is None:
        print_error("Không thể thực hiện dự đoán!")
        return
    
    # Step 5: Display results
    display_results(result)
    
    print_header("✨ HOÀN THÀNH")

if __name__ == "__main__":
    main()
