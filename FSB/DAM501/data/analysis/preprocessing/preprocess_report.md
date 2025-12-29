# Preprocessing Analysis Report

## Dataset Overview

| Dataset | Rows | Columns | Min Datetime | Max Datetime | Unique Datetimes | Duplicates | Parse Errors |
|---|---:|---:|---|---|---:|---:|---:|
| air_quality | 25429 | 8 | 2022-12-31 17:00:00 | 2025-12-29 11:00:00 | 25429 | 0 | 0 |
| weather | 25393 | 12 | 2022-12-31 17:00:00 | 2025-12-29 04:00:00 | 25393 | 0 | 0 |
| holidays | 24024 | 3 | 2022-12-31 17:00:00 | 2025-10-30 16:00:00 | 24024 | 0 | 0 |
| traffic | 24816 | 4 | 2022-12-31 17:00:00 | 2025-10-30 16:00:00 | 24816 | 0 | 0 |

## Time Coverage & Gaps

| Dataset | Expected Hours | Missing Hours | Gap Segments | Max Gap (hours) |
|---|---:|---:|---:|---:|
| air_quality | 26251 | 822 | 36 | 24.0 |
| weather | 26244 | 851 | 36 | 25.0 |
| holidays | 24816 | 792 | 33 | 25.0 |
| traffic | 24816 | 0 | 0 | 0.0 |

## Missing Values (Top 5 per Dataset)

### air_quality

| Column | Missing Count |
|---|---:|
| datetime | 0 |
| aqi | 0 |
| pm25 | 0 |
| pm10 | 0 |
| o3 | 0 |

### weather

| Column | Missing Count |
|---|---:|
| vis | 7 |
| datetime | 0 |
| temp | 0 |
| app_temp | 0 |
| rh | 0 |

### holidays

| Column | Missing Count |
|---|---:|
| holiday_name | 23307 |
| datetime | 0 |
| is_holiday | 0 |

### traffic

| Column | Missing Count |
|---|---:|
| datetime | 0 |
| is_holiday | 0 |
| congestion_index | 0 |
| congestion_noise | 0 |

## Alignment Between Sources

- Common timestamps (air ∩ weather): 25392
- Common timestamps (all sources): 24024
- Coverage vs air+weather base:
  - air_quality: 100.00%
  - weather: 100.00%
  - holidays: 94.61%
  - traffic: 94.61%

## Key Findings

- Time ranges are not fully aligned across sources (air/weather extend beyond holidays/traffic).
- Missing values exist in multiple columns; see per-dataset tables above.
- Hourly gaps and duplicate timestamps may affect merge consistency.

## Recommended Preprocessing Actions

1) Align time ranges across datasets before merge (clip to common window).
2) Deduplicate by datetime after ingest (keep latest or aggregate).
3) Impute or drop missing values per variable policy.
4) Validate hourly continuity; fill gaps if needed for rolling/lag features.