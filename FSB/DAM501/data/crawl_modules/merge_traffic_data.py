#!/usr/bin/env python3
"""
Script merge dữ liệu traffic thực từ TomTom với traffic proxy cũ
Để có đầy đủ dữ liệu lịch sử cho training
"""

import pandas as pd
import numpy as np
from datetime import datetime

TOMTOM_FILE = '../data_file/hanoi_tomtom_traffic.csv'
PROXY_FILE = '../data_file/hanoi_traffic_proxy.csv'
OUTPUT_FILE = '../data_file/hanoi_traffic_merged.csv'

def merge_traffic_data():
    """Merge TomTom real data với proxy data"""
    
    print("🔄 MERGE TRAFFIC DATA")
    print("="*70)
    
    # Load TomTom data (real)
    try:
        df_tomtom = pd.read_csv(TOMTOM_FILE)
        df_tomtom['datetime'] = pd.to_datetime(df_tomtom['datetime'], format='%Y-%m-%d:%H')
        df_tomtom['source'] = 'tomtom'
        print(f"✅ TomTom data: {len(df_tomtom)} records")
        print(f"   Latest: {df_tomtom['datetime'].max()}")
    except FileNotFoundError:
        print("⚠️  Chưa có TomTom data")
        df_tomtom = pd.DataFrame()
    
    # Load Proxy data (fake)
    df_proxy = pd.read_csv(PROXY_FILE)
    df_proxy['datetime'] = pd.to_datetime(df_proxy['datetime'])
    df_proxy['source'] = 'proxy'
    print(f"✅ Proxy data: {len(df_proxy)} records")
    
    if len(df_tomtom) > 0:
        # Chỉ lấy proxy data TRƯỚC khi có TomTom data
        tomtom_start = df_tomtom['datetime'].min()
        df_proxy_old = df_proxy[df_proxy['datetime'] < tomtom_start].copy()
        
        print(f"\n📊 Merge strategy:")
        print(f"   Proxy data (before {tomtom_start}): {len(df_proxy_old)} records")
        print(f"   TomTom data (from {tomtom_start}): {len(df_tomtom)} records")
        
        # Combine
        df_merged = pd.concat([df_tomtom, df_proxy_old], ignore_index=True)
    else:
        print(f"\n⚠️  Chưa có TomTom data, sử dụng Proxy")
        df_merged = df_proxy.copy()
    
    # Sort
    df_merged = df_merged.sort_values('datetime', ascending=False).reset_index(drop=True)
    
    # Format datetime
    df_merged['datetime'] = df_merged['datetime'].dt.strftime('%Y-%m-%d:%H')
    
    # Select columns
    output_cols = ['datetime', 'congestion_index', 'source']
    if 'avg_speed' in df_merged.columns:
        output_cols.append('avg_speed')
    if 'congestion_noise' in df_merged.columns:
        output_cols.append('congestion_noise')
    else:
        df_merged['congestion_noise'] = 0
    
    df_output = df_merged[output_cols].copy()
    
    # Save
    df_output.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n✅ Đã lưu merged data:")
    print(f"   File: {OUTPUT_FILE}")
    print(f"   Total records: {len(df_output)}")
    print(f"   TomTom: {len(df_output[df_output['source']=='tomtom'])}")
    print(f"   Proxy: {len(df_output[df_output['source']=='proxy'])}")
    
    # Statistics
    print(f"\n📊 Statistics:")
    print(f"   Congestion Index - Mean: {df_output['congestion_index'].mean():.2f}")
    print(f"   Congestion Index - Std: {df_output['congestion_index'].std():.2f}")
    print(f"   Congestion Index - Range: {df_output['congestion_index'].min():.0f} - {df_output['congestion_index'].max():.0f}")

if __name__ == "__main__":
    merge_traffic_data()
