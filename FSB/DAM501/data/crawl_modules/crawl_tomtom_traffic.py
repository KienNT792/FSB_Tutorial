#!/usr/bin/env python3
"""
Script thu thập dữ liệu traffic thực từ TomTom Traffic API
Thay thế traffic proxy giả bằng dữ liệu thực
"""

import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import os
import numpy as np

# ===== CẤU HÌNH =====
# Đăng ký free API key tại: https://developer.tomtom.com/
TOMTOM_API_KEY = "6vid7SpiMSozPPibYsUWJlMLxDzIfkxv"  # Thay bằng API key của bạn

# Các tuyến đường chính ở Hà Nội (tọa độ start-end)
HANOI_ROUTES = [
    {
        'name': 'Nguyễn Trãi - Khuất Duy Tiến',
        'points': '21.0015,105.8195:21.0295,105.8342',  # Nam -> Bắc
        'zoom': 12
    },
    {
        'name': 'Giải Phóng - Trường Chinh', 
        'points': '20.9985,105.8435:21.0245,105.8265',  # Đông -> Tây
        'zoom': 12
    },
    {
        'name': 'Láng Hạ - Thái Hà',
        'points': '21.0165,105.8095:21.0295,105.8195',  # Trung tâm
        'zoom': 13
    },
    {
        'name': 'Cầu Giấy - Xuân Thủy',
        'points': '21.0315,105.7895:21.0435,105.8025',  # Tây Bắc
        'zoom': 13
    },
    {
        'name': 'Kim Mã - Nguyễn Chí Thanh',
        'points': '21.0295,105.8165:21.0385,105.8125',  # Trung tâm
        'zoom': 13
    }
]

OUTPUT_FILE = '../data_file/hanoi_tomtom_traffic.csv'

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def get_traffic_flow(route, api_key):
    """
    Lấy traffic flow data từ TomTom API
    
    API: https://api.tomtom.com/traffic/services/4/flowSegmentData
    """
    # Parse points
    points = route['points'].split(':')
    lat, lon = points[0].split(',')
    
    url = 'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/{zoom}/json'
    
    params = {
        'key': api_key,
        'point': f'{lat},{lon}',
        'unit': 'KMPH'
    }
    
    try:
        response = requests.get(
            url.format(zoom=route['zoom']), 
            params=params, 
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if 'flowSegmentData' in data:
            flow = data['flowSegmentData']
            return {
                'route': route['name'],
                'current_speed': flow.get('currentSpeed', 0),
                'free_flow_speed': flow.get('freeFlowSpeed', 50),
                'current_travel_time': flow.get('currentTravelTime', 0),
                'free_flow_travel_time': flow.get('freeFlowTravelTime', 0),
                'confidence': flow.get('confidence', 0.5),
                'road_closure': flow.get('roadClosure', False)
            }
        else:
            return None
            
    except Exception as e:
        print(f"{Colors.RED}   ❌ Lỗi {route['name']}: {e}{Colors.END}")
        return None

def calculate_congestion_index(traffic_data):
    """
    Tính chỉ số tắc nghẽn từ traffic flow data
    
    Công thức:
    - Congestion Index = 100 * (1 - current_speed / free_flow_speed)
    - 0 = không tắc, 100 = tắc hoàn toàn
    """
    if not traffic_data:
        return None
    
    current = traffic_data['current_speed']
    free_flow = traffic_data['free_flow_speed']
    
    if free_flow == 0:
        return 50  # Default
    
    # Tính tỷ lệ giảm tốc
    speed_ratio = current / free_flow
    
    # Congestion index: 0-100
    # 0 = flowing freely, 100 = stopped
    congestion = 100 * (1 - speed_ratio)
    
    # Weight by confidence
    confidence = traffic_data.get('confidence', 0.5)
    weighted_congestion = congestion * confidence
    
    return max(0, min(100, weighted_congestion))

def fetch_current_traffic(api_key):
    """Lấy traffic data hiện tại cho tất cả các tuyến"""
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}Thu thập Traffic Data từ TomTom API{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")
    
    current_time = datetime.now()
    print(f"{Colors.BLUE}⏰ Thời gian: {current_time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}\n")
    
    all_traffic = []
    
    for i, route in enumerate(HANOI_ROUTES, 1):
        print(f"{Colors.BLUE}[{i}/{len(HANOI_ROUTES)}] {route['name']}...{Colors.END}", end=' ')
        
        traffic = get_traffic_flow(route, api_key)
        
        if traffic:
            congestion = calculate_congestion_index(traffic)
            traffic['congestion_index'] = congestion
            all_traffic.append(traffic)
            
            print(f"{Colors.GREEN}✓ Speed: {traffic['current_speed']:.0f}/{traffic['free_flow_speed']:.0f} km/h, "
                  f"Congestion: {congestion:.1f}{Colors.END}")
        else:
            print(f"{Colors.RED}✗{Colors.END}")
        
        time.sleep(0.2)  # Rate limiting
    
    if not all_traffic:
        print(f"\n{Colors.RED}❌ Không lấy được dữ liệu nào!{Colors.END}")
        return None
    
    # Tính trung bình cho toàn thành phố
    avg_congestion = np.mean([t['congestion_index'] for t in all_traffic])
    avg_speed = np.mean([t['current_speed'] for t in all_traffic])
    avg_free_speed = np.mean([t['free_flow_speed'] for t in all_traffic])
    
    print(f"\n{Colors.BOLD}📊 Kết quả tổng hợp:{Colors.END}")
    print(f"   Tốc độ TB: {avg_speed:.1f} km/h (free flow: {avg_free_speed:.1f} km/h)")
    print(f"   Congestion Index: {avg_congestion:.1f}")
    
    return {
        'datetime': current_time.strftime('%Y-%m-%d:%H'),
        'congestion_index': avg_congestion,
        'avg_speed': avg_speed,
        'free_flow_speed': avg_free_speed,
        'num_routes': len(all_traffic)
    }

def save_traffic_data(traffic_record):
    """Lưu traffic data vào CSV"""
    
    if not traffic_record:
        return
    
    # Load existing data nếu có
    if os.path.exists(OUTPUT_FILE):
        df_existing = pd.read_csv(OUTPUT_FILE)
        df_existing['datetime'] = pd.to_datetime(df_existing['datetime'], format='%Y-%m-%d:%H')
    else:
        df_existing = pd.DataFrame()
    
    # Create new record
    df_new = pd.DataFrame([traffic_record])
    df_new['datetime'] = pd.to_datetime(df_new['datetime'], format='%Y-%m-%d:%H')
    
    # Merge
    if len(df_existing) > 0:
        # Remove duplicate datetime
        df_existing = df_existing[
            df_existing['datetime'] != df_new['datetime'].iloc[0]
        ]
        df_combined = pd.concat([df_new, df_existing], ignore_index=True)
    else:
        df_combined = df_new
    
    # Sort by datetime descending
    df_combined = df_combined.sort_values('datetime', ascending=False).reset_index(drop=True)
    
    # Format datetime back
    df_combined['datetime'] = df_combined['datetime'].dt.strftime('%Y-%m-%d:%H')
    
    # Save
    df_combined.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n{Colors.GREEN}✅ Đã lưu vào {OUTPUT_FILE}{Colors.END}")
    print(f"   Tổng số records: {len(df_combined)}")

def setup_instructions():
    """Hướng dẫn setup"""
    print(f"{Colors.BOLD}{Colors.YELLOW}╔{'═'*68}╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}║{' '*68}║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}║  HƯỚNG DẪN CÀI ĐẶT TOMTOM TRAFFIC API{' '*30}║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}║{' '*68}║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}╚{'═'*68}╝{Colors.END}\n")
    
    print(f"{Colors.BOLD}Bước 1: Đăng ký TomTom Developer Account{Colors.END}")
    print(f"   🌐 Truy cập: https://developer.tomtom.com/")
    print(f"   📝 Đăng ký tài khoản miễn phí\n")
    
    print(f"{Colors.BOLD}Bước 2: Tạo API Key{Colors.END}")
    print(f"   1. Đăng nhập vào TomTom Developer Portal")
    print(f"   2. Vào 'Dashboard' → 'API Keys'")
    print(f"   3. Click 'Create API Key'")
    print(f"   4. Chọn products: 'Traffic API'")
    print(f"   5. Copy API key\n")
    
    print(f"{Colors.BOLD}Bước 3: Cấu hình Script{Colors.END}")
    print(f"   📝 Mở file: {Colors.BLUE}crawl_tomtom_traffic.py{Colors.END}")
    print(f"   ✏️  Dòng 18: Thay 'YOUR_API_KEY_HERE' bằng API key của bạn\n")
    
    print(f"{Colors.BOLD}Bước 4: Chạy Script{Colors.END}")
    print(f"   {Colors.GREEN}python crawl_tomtom_traffic.py{Colors.END}\n")
    
    print(f"{Colors.BOLD}📊 Free Tier Limits:{Colors.END}")
    print(f"   • 2,500 transactions/day")
    print(f"   • 5 requests/second")
    print(f"   • Đủ cho collect 1 record/giờ trong 100+ ngày\n")
    
    print(f"{Colors.BOLD}🔄 Tự động hóa với Cron:{Colors.END}")
    print(f"   {Colors.BLUE}0 * * * * cd /path/to/crawl_modules && python crawl_tomtom_traffic.py{Colors.END}")
    print(f"   (Chạy mỗi giờ)\n")

def main():
    """Main function"""
    
    if TOMTOM_API_KEY == "YOUR_API_KEY_HERE":
        setup_instructions()
        print(f"{Colors.RED}❌ Chưa cấu hình API Key!{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  Làm theo hướng dẫn ở trên để setup.{Colors.END}\n")
        return
    
    # Fetch traffic data
    traffic_record = fetch_current_traffic(TOMTOM_API_KEY)
    
    # Save to file
    if traffic_record:
        save_traffic_data(traffic_record)
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}✨ Thành công!{Colors.END}")
        print(f"{Colors.BLUE}💡 Setup cron job để thu thập tự động mỗi giờ{Colors.END}\n")
    else:
        print(f"\n{Colors.RED}❌ Thu thập thất bại{Colors.END}\n")

if __name__ == "__main__":
    main()
