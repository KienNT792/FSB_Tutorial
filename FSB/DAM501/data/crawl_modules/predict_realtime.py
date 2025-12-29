#!/usr/bin/env python3
"""
Script dự đoán PM2.5 cho 1 giờ tới - PHIÊN BẢN REALTIME
Sử dụng dữ liệu mới nhất, tự động fill missing values
"""

import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Cấu hình
DATA_PATH = '../data_file/'
MODEL_PATH = '../notebook/output/'
MODEL_FILE = 'xgboost_model_1h.pkl'

# Colors
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

def load_and_prepare_data():
    """Load dữ liệu và chuẩn bị cho dự đoán realtime"""
    print_header("BƯỚC 1: LOAD VÀ XỬ LÝ DỮ LIỆU")
    
    # Load datasets
    air = pd.read_csv(f'{DATA_PATH}hanoi_air_quality_history.csv')
    weather = pd.read_csv(f'{DATA_PATH}hanoi_weather_history.csv')
    holidays = pd.read_csv(f'{DATA_PATH}hanoi_holidays_aligned.csv')
    traffic = pd.read_csv(f'{DATA_PATH}hanoi_traffic_proxy.csv')
    
    air['datetime'] = pd.to_datetime(air['datetime'], format='%Y-%m-%d:%H')
    weather['datetime'] = pd.to_datetime(weather['datetime'], format='%Y-%m-%d:%H')
    holidays['datetime'] = pd.to_datetime(holidays['datetime'])
    traffic['datetime'] = pd.to_datetime(traffic['datetime'])
    
    print_info(f"Air: {len(air)} records → {air['datetime'].max()}")
    print_info(f"Weather: {len(weather)} records → {weather['datetime'].max()}")
    
    # Merge với LEFT JOIN
    df = pd.merge(air, weather, on='datetime', how='left')
    df = pd.merge(df, holidays[['datetime', 'is_holiday', 'holiday_name']], 
                 on='datetime', how='left')
    df = pd.merge(df, traffic[['datetime', 'congestion_index', 'congestion_noise']], 
                 on='datetime', how='left')
    
    df = df.sort_values('datetime').reset_index(drop=True)
    
    # Forward fill missing data
    weather_cols = ['temp', 'rh', 'wind_spd', 'wind_dir', 'pres', 'vis', 'clouds', 'precip']
    for col in weather_cols:
        if col in df.columns:
            df[col] = df[col].ffill()
    
    df['is_holiday'] = df['is_holiday'].fillna(0).astype(int)
    df['holiday_name'] = df['holiday_name'].fillna('')
    df['congestion_index'] = df['congestion_index'].ffill().fillna(df['congestion_index'].median())
    df['congestion_noise'] = df['congestion_noise'].fillna(0)
    
    print_success(f"Merged: {len(df)} records → {df['datetime'].max()}")
    
    return df

def engineer_features_smart(df):
    """Feature engineering với smart missing value handling"""
    print_header("BƯỚC 2: FEATURE ENGINEERING (SMART MODE)")
    
    df = df.copy()
    
    # Time features
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['month'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    
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
        df[f'pm25_roll_mean_{win}'] = df['pm25'].rolling(win, min_periods=1).mean()
        df[f'pm25_roll_std_{win}'] = df['pm25'].rolling(win, min_periods=1).std()
        df[f'pm25_roll_min_{win}'] = df['pm25'].rolling(win, min_periods=1).min()
        df[f'pm25_roll_max_{win}'] = df['pm25'].rolling(win, min_periods=1).max()
    
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
        q75 = df['congestion_index'].quantile(0.75)
        q25 = df['congestion_index'].quantile(0.25)
        df['high_traffic'] = (df['congestion_index'] > q75).astype(int)
        df['low_traffic'] = (df['congestion_index'] < q25).astype(int)
    
    print_info("Tạo interaction features...")
    # Interaction features
    df['temp_x_rh'] = df['temp'] * df['rh']
    df['wind_spd_x_temp'] = df['wind_spd'] * df['temp']
    
    if 'congestion_index' in df.columns:
        df['traffic_x_hour'] = df['congestion_index'] * df['hour']
        df['traffic_x_holiday'] = df['congestion_index'] * df.get('is_holiday', 0)
        df['pm25_x_traffic'] = df['pm25'] * df['congestion_index']
    
    print_success(f"Created {df.shape[1]} features")
    
    # CRITICAL: Fill remaining NaN values để có thể dự đoán record mới nhất
    print_warning("Filling remaining NaN values for realtime prediction...")
    
    # Fill lag features với giá trị trước đó hoặc mean
    for col in df.columns:
        if col not in ['datetime', 'holiday_name']:
            # First try forward fill
            df[col] = df[col].ffill()
            # Then backward fill
            df[col] = df[col].bfill()
            # Finally fill any remaining with median
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].fillna(df[col].median())
    
    print_info(f"NaN count after fill: {df.isnull().sum().sum()}")
    
    return df

def predict_realtime(df):
    """Dự đoán với dữ liệu realtime mới nhất"""
    print_header("BƯỚC 3: DỰ ĐOÁN REALTIME")
    
    # Load model
    model_path = f'{MODEL_PATH}{MODEL_FILE}'
    print_info(f"Loading model from {model_path}...")
    model = joblib.load(model_path)
    print_success("Model loaded!")
    
    # Prepare features
    exclude_cols = ['datetime', 'pm25', 'target', 'holiday_name']
    features = [c for c in df.columns if c not in exclude_cols]
    
    # TEST MODE: Lấy dữ liệu của NGÀY HÔM QUA để có thể verify
    # Filter chỉ lấy data đến hết ngày hôm qua
    yesterday = datetime.now().date() - timedelta(days=1)
    df_yesterday = df[df['datetime'].dt.date <= yesterday].copy()
    
    print_warning(f"TEST MODE: Sử dụng dữ liệu đến {yesterday}")
    
    # Get LATEST record của ngày hôm qua
    latest_idx = df_yesterday['datetime'].idxmax()
    latest_record = df_yesterday.loc[latest_idx]
    
    current_pm25 = latest_record['pm25']
    current_time = latest_record['datetime']
    
    print_info(f"📅 Thời gian dữ liệu: {current_time}")
    print_info(f"🌫️  PM2.5 hiện tại: {current_pm25:.2f} μg/m³")
    
    # Check for NaN in features
    feature_values = latest_record[features]
    nan_count = feature_values.isnull().sum()
    if nan_count > 0:
        print_warning(f"Record có {nan_count} NaN features, đã được fill tự động")
    
    # Make prediction
    X = feature_values.values.reshape(1, -1)
    prediction = model.predict(X)[0]
    forecast_time = current_time + timedelta(hours=1)
    
    print_success("Dự đoán thành công!")
    
    # Tìm giá trị thực tế (actual) nếu có
    actual_pm25 = None
    actual_record = df[df['datetime'] == forecast_time]
    if len(actual_record) > 0:
        actual_pm25 = actual_record.iloc[0]['pm25']
        print_info(f"✓ Tìm thấy giá trị thực tế tại {forecast_time}: {actual_pm25:.2f} μg/m³")
    
    return {
        'current_time': current_time,
        'forecast_time': forecast_time,
        'current_pm25': current_pm25,
        'predicted_pm25': prediction,
        'actual_pm25': actual_pm25,
        'change': prediction - current_pm25,
        'change_pct': (prediction - current_pm25) / current_pm25 * 100,
        'nan_features': nan_count
    }

def get_aqi_level(pm25):
    """Xác định mức độ AQI"""
    if pm25 <= 12:
        return "TỐT", Colors.GREEN
    elif pm25 <= 35.4:
        return "TRUNG BÌNH", Colors.BLUE
    elif pm25 <= 55.4:
        return "KÉM", Colors.YELLOW
    elif pm25 <= 150.4:
        return "XẤU", Colors.RED
    else:
        return "NGUY HIỂM", Colors.RED

def display_results(result):
    """Hiển thị kết quả"""
    print_header("KẾT QUẢ DỰ ĐOÁN PM2.5 REALTIME - 1 GIỜ TỚI")
    
    # Current
    current_level, current_color = get_aqi_level(result['current_pm25'])
    print(f"{Colors.BOLD}📍 DỮ LIỆU HIỆN TẠI ({result['current_time'].strftime('%Y-%m-%d %H:%M')}){Colors.END}")
    print(f"   PM2.5: {current_color}{result['current_pm25']:.2f} μg/m³{Colors.END}")
    print(f"   Mức độ: {current_color}{current_level}{Colors.END}")
    
    print()
    
    # Forecast
    forecast_level, forecast_color = get_aqi_level(result['predicted_pm25'])
    print(f"{Colors.BOLD}🔮 DỰ ĐOÁN ({result['forecast_time'].strftime('%Y-%m-%d %H:%M')}){Colors.END}")
    print(f"   PM2.5: {forecast_color}{result['predicted_pm25']:.2f} μg/m³{Colors.END}")
    print(f"   Mức độ: {forecast_color}{forecast_level}{Colors.END}")
    
    # Actual value if available
    if result['actual_pm25'] is not None:
        actual_level, actual_color = get_aqi_level(result['actual_pm25'])
        print()
        print(f"{Colors.BOLD}✅ THỰC TẾ ({result['forecast_time'].strftime('%Y-%m-%d %H:%M')}){Colors.END}")
        print(f"   PM2.5: {actual_color}{result['actual_pm25']:.2f} μg/m³{Colors.END}")
        print(f"   Mức độ: {actual_color}{actual_level}{Colors.END}")
        
        # Prediction error
        error = result['predicted_pm25'] - result['actual_pm25']
        abs_error = abs(error)
        error_pct = abs_error / result['actual_pm25'] * 100
        
        print()
        print(f"{Colors.BOLD}📊 ĐỘ CHÍNH XÁC{Colors.END}")
        print(f"   Sai số: {error:+.2f} μg/m³")
        print(f"   |Sai số|: {abs_error:.2f} μg/m³ ({error_pct:.1f}%)")
        
        if abs_error < 10:
            print(f"   {Colors.GREEN}✓ Dự đoán RẤT TỐT (sai số < 10){Colors.END}")
        elif abs_error < 15:
            print(f"   {Colors.BLUE}✓ Dự đoán TỐT (sai số < 15){Colors.END}")
        elif abs_error < 20:
            print(f"   {Colors.YELLOW}○ Dự đoán CHẤP NHẬN ĐƯỢC (sai số < 20){Colors.END}")
        else:
            print(f"   {Colors.RED}⚠ Sai số lớn (> 20){Colors.END}")
    
    print()
    
    # Change
    change_symbol = "📈" if result['change'] > 0 else "📉" if result['change'] < 0 else "➡️"
    change_color = Colors.RED if result['change'] > 0 else Colors.GREEN if result['change'] < 0 else Colors.BLUE
    
    print(f"{Colors.BOLD}📊 THAY ĐỔI DỰ ĐOÁN{Colors.END}")
    print(f"   {change_symbol} {change_color}{result['change']:+.2f} μg/m³ ({result['change_pct']:+.1f}%){Colors.END}")
    
    if result['nan_features'] > 0:
        print()
        print_warning(f"Dự đoán sử dụng {result['nan_features']} features được fill tự động")
    
    print()
    
    # Recommendations
    print(f"{Colors.BOLD}💡 KHUYẾN NGHỊ{Colors.END}")
    if result['predicted_pm25'] > 55.4:
        print(f"   {Colors.RED}⚠️  Chất lượng không khí XẤU - Hạn chế ra ngoài{Colors.END}")
        print(f"   {Colors.RED}⚠️  Đeo khẩu trang khi ra đường{Colors.END}")
    elif result['predicted_pm25'] > 35.4:
        print(f"   {Colors.YELLOW}⚠️  Chất lượng không khí KÉM - Cẩn thận{Colors.END}")
    else:
        print(f"   {Colors.GREEN}✓ Chất lượng không khí ở mức chấp nhận được{Colors.END}")

def main():
    """Main function"""
    print_header("🌫️  REALTIME PM2.5 FORECASTING - TEST MODE")
    print(f"{Colors.BOLD}Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print(f"{Colors.YELLOW}⚠️  TEST MODE: Sử dụng dữ liệu ngày hôm qua để verify kết quả{Colors.END}")
    
    df = load_and_prepare_data()
    df_feat = engineer_features_smart(df)
    result = predict_realtime(df_feat)
    display_results(result)
    
    print_header("✨ HOÀN THÀNH")

if __name__ == "__main__":
    main()
