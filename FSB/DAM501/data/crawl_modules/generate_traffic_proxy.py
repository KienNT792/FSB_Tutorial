#!/usr/bin/env python3
"""
Hanoi Traffic Proxy Generator
-----------------------------
Dựa vào ngày lễ (hanoi_holidays_aligned.csv) và các giờ cao điểm,
sinh ra một cột `congestion_index` (0‑100) mô phỏng mật độ giao thông.

Output: data/data_file/hanoi_traffic_proxy.csv
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------
DATA_DIR   = os.path.abspath(os.path.join(__file__, "../../data_file"))
HOLIDAY_F  = os.path.join(DATA_DIR, "hanoi_holidays_aligned.csv")
OUT_FILE   = os.path.join(DATA_DIR, "hanoi_traffic_proxy.csv")

# ----------------------------------------------------------------------
# 1. Load holiday table (datetime, is_holiday, holiday_name)
# ----------------------------------------------------------------------
holidays = pd.read_csv(HOLIDAY_F)
holidays["datetime"] = pd.to_datetime(holidays["datetime"])

# ----------------------------------------------------------------------
# 2. Build a full hourly index covering the whole holiday range
# ----------------------------------------------------------------------
start_dt = holidays["datetime"].min()
end_dt   = holidays["datetime"].max()
hourly   = pd.DataFrame({"datetime": pd.date_range(start_dt, end_dt, freq="h")})

# ----------------------------------------------------------------------
# 3. Merge holiday flag
# ----------------------------------------------------------------------
hourly = hourly.merge(holidays[["datetime", "is_holiday"]], on="datetime", how="left")
hourly["is_holiday"] = hourly["is_holiday"].fillna(0).astype(int)

# ----------------------------------------------------------------------
# 4. Base traffic level
#    - Non‑holiday: 40‑70 (medium)
#    - Holiday:    10‑30 (low)
# ----------------------------------------------------------------------
np.random.seed(42)  # reproducible
base = np.where(
    hourly["is_holiday"] == 1,
    np.random.randint(10, 31, size=len(hourly)),   # holiday low traffic
    np.random.randint(40, 71, size=len(hourly)),   # normal traffic
)

# ----------------------------------------------------------------------
# 5. Add peak‑hour boost
#    Morning 7‑9 h  → +20‑30
#    Evening 17‑19 h → +20‑30
# ----------------------------------------------------------------------
hour = hourly["datetime"].dt.hour
peak_morning = (hour >= 7) & (hour <= 9)
peak_evening = (hour >= 17) & (hour <= 19)

peak_boost = np.where(
    peak_morning | peak_evening,
    np.random.randint(20, 31, size=len(hourly)),
    0,
)

# ----------------------------------------------------------------------
# 6. Final congestion index (clip 0‑100)
# ----------------------------------------------------------------------
hourly["congestion_index"] = np.clip(base + peak_boost, 0, 100)

# ----------------------------------------------------------------------
# 7. Optional: add a tiny random noise column (optional for realism)
# ----------------------------------------------------------------------
hourly["congestion_noise"] = np.random.normal(0, 2, size=len(hourly)).round(2)

# ----------------------------------------------------------------------
# 8. Save
# ----------------------------------------------------------------------
os.makedirs(DATA_DIR, exist_ok=True)
hourly.to_csv(OUT_FILE, index=False)
print(f"✅ Proxy traffic saved → {OUT_FILE}")
print(f"   Rows: {len(hourly):,}  |  Columns: {list(hourly.columns)}")