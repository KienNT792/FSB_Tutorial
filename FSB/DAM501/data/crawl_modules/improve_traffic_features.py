#!/usr/bin/env python3
"""
Cải thiện Traffic Features cho mô hình dự đoán PM2.5
Thêm các features nhìn về tương lai thay vì quá khứ
"""

import pandas as pd
import numpy as np

def add_forward_traffic_features(df):
    """
    Thêm các traffic features nhìn về TƯƠNG LAI
    Vì chúng ta dự đoán PM2.5 sau 1h, nên cần biết traffic sẽ như thế nào
    """
    df = df.copy()
    
    print("🚗 Thêm Forward Traffic Features...")
    
    # 1. Traffic trend (xu hướng tăng/giảm)
    df['traffic_diff_1h'] = df['congestion_index'].diff(1)
    df['traffic_diff_3h'] = df['congestion_index'].diff(3)
    
    # 2. Traffic rate of change (tốc độ thay đổi)
    df['traffic_roc_1h'] = df['congestion_index'].pct_change(1)
    df['traffic_roc_3h'] = df['congestion_index'].pct_change(3)
    
    # 3. Traffic acceleration (gia tốc thay đổi)
    df['traffic_accel'] = df['traffic_diff_1h'].diff(1)
    
    # 4. Upcoming peak hour (giờ cao điểm sắp tới)
    df['next_hour'] = (df['hour'] + 1) % 24
    df['is_next_peak'] = df['next_hour'].apply(
        lambda x: 1 if x in [7, 8, 9, 17, 18, 19] else 0
    )
    df['is_entering_peak'] = ((df['is_peak_hour'] == 0) & (df['is_next_peak'] == 1)).astype(int)
    df['is_leaving_peak'] = ((df['is_peak_hour'] == 1) & (df['is_next_peak'] == 0)).astype(int)
    
    # 5. Traffic momentum (động lượng)
    windows = [3, 6, 12]
    for win in windows:
        df[f'traffic_momentum_{win}h'] = (
            df['congestion_index'] - df['congestion_index'].rolling(win).mean()
        )
    
    # 6. Peak transition indicators
    df['peak_transition_score'] = 0
    # Sáng: 6h->7h, 9h->10h
    df.loc[df['hour'] == 6, 'peak_transition_score'] = 2  # Sắp vào peak
    df.loc[df['hour'] == 9, 'peak_transition_score'] = -2  # Sắp ra khỏi peak
    # Chiều: 16h->17h, 19h->20h
    df.loc[df['hour'] == 16, 'peak_transition_score'] = 2  # Sắp vào peak
    df.loc[df['hour'] == 19, 'peak_transition_score'] = -2  # Sắp ra khỏi peak
    
    # 7. Time to next peak (giờ đến peak tiếp theo)
    def time_to_next_peak(hour):
        if hour < 7:
            return 7 - hour
        elif hour < 17:
            return 17 - hour
        else:
            return 24 - hour + 7  # Đến sáng hôm sau
    
    df['hours_to_next_peak'] = df['hour'].apply(time_to_next_peak)
    
    # 8. Interaction: PM2.5 lag × upcoming traffic
    df['pm25_lag1_x_next_peak'] = df['pm25_lag_1'] * df['is_next_peak']
    df['pm25_lag1_x_entering_peak'] = df['pm25_lag_1'] * df['is_entering_peak']
    
    # 9. Traffic × Time interactions  
    df['traffic_x_sin_hour'] = df['congestion_index'] * df['hour_sin']
    df['traffic_x_cos_hour'] = df['congestion_index'] * df['hour_cos']
    
    # 10. Historical peak comparison
    # So sánh traffic hiện tại với trung bình của giờ này
    hourly_avg = df.groupby('hour')['congestion_index'].transform('mean')
    df['traffic_vs_hourly_avg'] = df['congestion_index'] - hourly_avg
    df['traffic_vs_hourly_ratio'] = df['congestion_index'] / (hourly_avg + 1)
    
    print(f"✅ Đã thêm {df.shape[1] - 89} forward traffic features")
    
    # Drop temporary columns
    df.drop(columns=['next_hour'], inplace=True, errors='ignore')
    
    return df

def analyze_traffic_impact():
    """Phân tích mối quan hệ traffic vs PM2.5"""
    print("📊 PHÂN TÍCH TRAFFIC VS PM2.5")
    print("="*70)
    
    # Load data
    air = pd.read_csv('../data_file/hanoi_air_quality_history.csv')
    traffic = pd.read_csv('../data_file/hanoi_traffic_proxy.csv')
    
    air['datetime'] = pd.to_datetime(air['datetime'], format='%Y-%m-%d:%H')
    traffic['datetime'] = pd.to_datetime(traffic['datetime'])
    
    df = pd.merge(air, traffic, on='datetime', how='inner')
    
    # PM2.5 theo giờ
    hourly_pm25 = df.groupby(df['datetime'].dt.hour)['pm25'].mean()
    hourly_traffic = df.groupby(df['datetime'].dt.hour)['congestion_index'].mean()
    
    print("\\nGiờ | Traffic | PM2.5  | Correlation")
    print("-" * 50)
    for hour in range(24):
        if hour in hourly_pm25.index:
            traffic_val = hourly_traffic[hour]
            pm25_val = hourly_pm25[hour]
            marker = "🔴" if hour in [7,8,9,17,18,19] else "  "
            print(f"{marker} {hour:02d}h | {traffic_val:6.1f} | {pm25_val:6.2f}")
    
    # Correlation
    corr = df[['congestion_index', 'pm25']].corr().iloc[0, 1]
    print(f"\\n💡 Overall correlation: {corr:.3f}")
    
    # Peak vs Non-peak
    peak_hours = [7, 8, 9, 17, 18, 19]
    df['is_peak'] = df['datetime'].dt.hour.isin(peak_hours)
    
    peak_pm25 = df[df['is_peak']]['pm25'].mean()
    nonpeak_pm25 = df[~df['is_peak']]['pm25'].mean()
    
    print(f"\\nPM2.5 giờ cao điểm: {peak_pm25:.2f} μg/m³")
    print(f"PM2.5 giờ bình thường: {nonpeak_pm25:.2f} μg/m³")
    print(f"Chênh lệch: {peak_pm25 - nonpeak_pm25:+.2f} μg/m³ ({(peak_pm25/nonpeak_pm25-1)*100:+.1f}%)")

if __name__ == "__main__":
    analyze_traffic_impact()
