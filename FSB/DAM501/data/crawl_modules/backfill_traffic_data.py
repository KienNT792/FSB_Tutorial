#!/usr/bin/env python3
"""
Backfill historical traffic data dựa trên pattern từ TomTom real data
Vì TomTom không có historical API miễn phí, ta sẽ:
1. Sử dụng real data hiện có làm mẫu
2. Tạo realistic pattern cho quá khứ
3. Thêm noise và variation hợp lý
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

TOMTOM_FILE = '../data_file/hanoi_tomtom_traffic.csv'
OUTPUT_FILE = '../data_file/hanoi_traffic_real_based.csv'
AIR_QUALITY_FILE = '../data_file/hanoi_air_quality_history.csv'

# Pattern từ TomTom real data (2025-12-29 12h)
REAL_SAMPLE = {
    'congestion_index': 20.36,
    'avg_speed': 26.0,
    'free_flow_speed': 33.0
}

def load_tomtom_sample():
    """Load TomTom sample nếu có, nếu không dùng default"""
    try:
        df = pd.read_csv(TOMTOM_FILE)
        if len(df) > 0:
            sample = df.iloc[0]
            return {
                'congestion_index': sample['congestion_index'],
                'avg_speed': sample.get('avg_speed', 26.0),
                'free_flow_speed': sample.get('free_flow_speed', 33.0)
            }
    except FileNotFoundError:
        pass
    return REAL_SAMPLE

def generate_hourly_pattern():
    """
    Tạo pattern hourly realistic dựa trên:
    - TomTom real data sample
    - Kinh nghiệm thực tế Hà Nội
    - Research về traffic pattern
    """
    
    # Base pattern (0-100 congestion index)
    pattern = {
        0: 10,   # 0h - rất thấp
        1: 8,    # 1h - rất thấp
        2: 7,    # 2h - thấp nhất
        3: 6,    # 3h - thấp nhất
        4: 8,    # 4h - bắt đầu tăng
        5: 12,   # 5h - sáng sớm
        6: 25,   # 6h - bắt đầu cao điểm
        7: 55,   # 7h - cao điểm sáng PEAK
        8: 60,   # 8h - cao điểm sáng MAX
        9: 45,   # 9h - giảm dần
        10: 25,  # 10h - trung bình
        11: 22,  # 11h - trước trưa
        12: 20,  # 12h - trưa (như real data: 20.36)
        13: 18,  # 13h - sau trưa
        14: 22,  # 14h - chiều
        15: 28,  # 15h - bắt đầu tăng
        16: 40,  # 16h - trước cao điểm
        17: 65,  # 17h - cao điểm chiều PEAK
        18: 70,  # 18h - cao điểm chiều MAX
        19: 50,  # 19h - giảm dần
        20: 30,  # 20h - tối
        21: 22,  # 21h - tối
        22: 15,  # 22h - đêm
        23: 12   # 23h - đêm
    }
    
    return pattern

def calculate_speed_from_congestion(congestion_index, base_free_flow=33.0):
    """
    Tính avg_speed từ congestion_index
    
    Formula: avg_speed = free_flow_speed * (1 - congestion_index/100)
    """
    speed_ratio = 1 - (congestion_index / 100)
    avg_speed = base_free_flow * speed_ratio
    
    # Min speed ~5 km/h (tắc hoàn toàn)
    return max(5.0, avg_speed)

def generate_realistic_traffic(start_date, end_date):
    """Tạo traffic data realistic cho khoảng thời gian"""
    
    print("🚗 Generating Realistic Traffic Data")
    print("="*70)
    print(f"Period: {start_date} → {end_date}")
    
    pattern = generate_hourly_pattern()
    
    # Generate hourly records
    current = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    records = []
    
    while current <= end:
        hour = current.hour
        base_congestion = pattern[hour]
        
        # Add realistic variations
        # 1. Day of week effect (weekend lower)
        dow_factor = 0.7 if current.weekday() >= 5 else 1.0
        
        # 2. Random noise (±15%)
        noise = np.random.uniform(-0.15, 0.15)
        
        # 3. Weather effect (giả lập - mưa tăng 20%)
        weather_factor = np.random.choice([1.0, 1.2], p=[0.8, 0.2])
        
        # Calculate final congestion
        congestion = base_congestion * dow_factor * weather_factor * (1 + noise)
        congestion = max(0, min(100, congestion))  # Clip 0-100
        
        # Calculate speed
        free_flow = 33.0  # km/h (from real data)
        avg_speed = calculate_speed_from_congestion(congestion, free_flow)
        
        records.append({
            'datetime': current.strftime('%Y-%m-%d:%H'),
            'congestion_index': congestion,
            'avg_speed': avg_speed,
            'free_flow_speed': free_flow,
            'source': 'generated',
            'day_of_week': current.strftime('%A'),
            'is_weekend': 1 if current.weekday() >= 5 else 0
        })
        
        current += timedelta(hours=1)
    
    df = pd.DataFrame(records)
    
    print(f"\n✅ Generated {len(df)} records")
    print(f"\n📊 Statistics:")
    print(f"   Congestion Index: {df['congestion_index'].mean():.1f} ± {df['congestion_index'].std():.1f}")
    print(f"   Avg Speed: {df['avg_speed'].mean():.1f} ± {df['avg_speed'].std():.1f} km/h")
    print(f"   Peak hours (17-18h): {df[df['datetime'].str.contains(':17|:18')]['congestion_index'].mean():.1f}")
    print(f"   Off-peak (2-4h): {df[df['datetime'].str.contains(':02|:03|:04')]['congestion_index'].mean():.1f}")
    
    return df

def merge_with_real_data(df_generated):
    """Merge generated data với real TomTom data"""
    
    try:
        df_real = pd.read_csv(TOMTOM_FILE)
        df_real['source'] = 'tomtom_real'
        
        print(f"\n🔄 Merging with real TomTom data...")
        print(f"   Real data: {len(df_real)} records")
        
        # Remove generated records that have real data
        real_datetimes = df_real['datetime'].tolist()
        df_generated = df_generated[~df_generated['datetime'].isin(real_datetimes)]
        
        # Combine
        df_combined = pd.concat([df_real, df_generated], ignore_index=True)
        df_combined = df_combined.sort_values('datetime', ascending=False).reset_index(drop=True)
        
        print(f"   Combined: {len(df_combined)} records")
        print(f"   Real: {len(df_combined[df_combined['source']=='tomtom_real'])}")
        print(f"   Generated: {len(df_combined[df_combined['source']=='generated'])}")
        
        return df_combined
        
    except FileNotFoundError:
        print("\n⚠️  No real TomTom data found, using only generated data")
        return df_generated

def main():
    """Main function"""
    
    # Load TomTom sample
    sample = load_tomtom_sample()
    print(f"Using sample: {sample}")
    
    # Get date range from air quality data
    try:
        df_air = pd.read_csv(AIR_QUALITY_FILE)
        df_air['datetime'] = pd.to_datetime(df_air['datetime'], format='%Y-%m-%d:%H')
        
        start_date = df_air['datetime'].min().strftime('%Y-%m-%d')
        end_date = df_air['datetime'].max().strftime('%Y-%m-%d')
        
        print(f"\n📅 Air quality data range: {start_date} → {end_date}")
        
    except Exception as e:
        print(f"⚠️  Cannot read air quality file: {e}")
        start_date = '2023-01-01'
        end_date = '2025-12-29'
    
    # Generate traffic data
    df_generated = generate_realistic_traffic(start_date, end_date)
    
    # Merge with real data if available
    df_final = merge_with_real_data(df_generated)
    
    # Save
    df_final.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n✅ Saved to {OUTPUT_FILE}")
    print(f"   Total records: {len(df_final)}")
    print(f"\n📊 Statistics:")
    print(df_final['congestion_index'].describe())
    
    print("="*70)
    print("BACKFILL HISTORICAL TRAFFIC DATA")
    print("="*70)
    print()
    
    # Generate từ 2023-01-01 đến hôm nay
    start_date = '2023-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Generate data
    df_generated = generate_realistic_traffic(start_date, end_date)
    
    # Merge với real data nếu có
    df_final = merge_with_real_data(df_generated)
    
    # Select columns
    output_cols = ['datetime', 'congestion_index', 'avg_speed', 'free_flow_speed', 'source']
    df_output = df_final[output_cols].copy()
    
    # Save
    df_output.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n✅ Saved to: {OUTPUT_FILE}")
    print(f"   Total records: {len(df_output):,}")
    
    # Validation
    print(f"\n🔍 Validation:")
    hourly_avg = pd.DataFrame({
        'datetime': pd.to_datetime(df_output['datetime'], format='%Y-%m-%d:%H')
    })
    hourly_avg['hour'] = hourly_avg['datetime'].dt.hour
    hourly_avg['congestion'] = df_output['congestion_index']
    
    hourly_pattern = hourly_avg.groupby('hour')['congestion'].mean()
    
    print(f"\n   Peak hours (7-9h): {hourly_pattern[[7,8,9]].mean():.1f}")
    print(f"   Peak hours (17-19h): {hourly_pattern[[17,18,19]].mean():.1f}")
    print(f"   Off-peak (2-5h): {hourly_pattern[[2,3,4,5]].mean():.1f}")
    
    print(f"\n💡 Next steps:")
    print(f"   1. Setup cron job để chạy crawl_tomtom_traffic.py mỗi giờ")
    print(f"   2. Sau vài tuần, sẽ có đủ real data")
    print(f"   3. Re-train model với traffic data mới")

if __name__ == "__main__":
    main()
