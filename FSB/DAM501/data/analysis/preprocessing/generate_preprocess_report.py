from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import csv

MISSING_TOKENS = {"", "nan", "NaN", "NULL", "null", "None", "none"}

@dataclass
class DatasetSpec:
    name: str
    path: str
    datetime_format: str


DATASETS = [
    DatasetSpec("air_quality", "data/data_file/hanoi_air_quality_history.csv", "%Y-%m-%d:%H"),
    DatasetSpec("weather", "data/data_file/hanoi_weather_history.csv", "%Y-%m-%d:%H"),
    DatasetSpec("holidays", "data/data_file/hanoi_holidays_aligned.csv", "%Y-%m-%d %H:%M:%S"),
    DatasetSpec("traffic", "data/data_file/hanoi_traffic_proxy.csv", "%Y-%m-%d %H:%M:%S"),
]


def _parse_dt(value: str, fmt: str) -> datetime | None:
    try:
        return datetime.strptime(value, fmt)
    except Exception:
        return None


def _missing(val: str) -> bool:
    return val.strip() in MISSING_TOKENS


def _gap_stats(dts: list[datetime]) -> tuple[int, int, float]:
    if len(dts) < 2:
        return 0, 0, 0.0
    dts_sorted = sorted(dts)
    missing_hours = 0
    gap_segments = 0
    max_gap_hours = 0.0
    prev = dts_sorted[0]
    for cur in dts_sorted[1:]:
        diff_hours = (cur - prev).total_seconds() / 3600.0
        if diff_hours > 1.0:
            gap_segments += 1
            missing_hours += int(diff_hours) - 1
            if diff_hours > max_gap_hours:
                max_gap_hours = diff_hours
        prev = cur
    return missing_hours, gap_segments, max_gap_hours


def analyze_dataset(spec: DatasetSpec) -> dict:
    path = Path(spec.path)
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {spec.path}")

    with path.open(newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        missing_counts = [0] * len(header)
        dt_set: set[datetime] = set()
        min_dt: datetime | None = None
        max_dt: datetime | None = None
        rows = 0
        parse_errors = 0

        for row in reader:
            if not row:
                continue
            rows += 1
            if len(row) < len(header):
                row += [""] * (len(header) - len(row))
            for i, val in enumerate(row[: len(header)]):
                if _missing(val):
                    missing_counts[i] += 1

            dt = _parse_dt(row[0].strip(), spec.datetime_format)
            if dt is None:
                parse_errors += 1
            else:
                dt_set.add(dt)
                if min_dt is None or dt < min_dt:
                    min_dt = dt
                if max_dt is None or dt > max_dt:
                    max_dt = dt

    unique_count = len(dt_set)
    duplicates = rows - unique_count

    expected = None
    missing_time = None
    if min_dt and max_dt:
        expected = int((max_dt - min_dt).total_seconds() / 3600) + 1
        missing_time = max(0, expected - unique_count)

    missing_hours, gap_segments, max_gap_hours = _gap_stats(list(dt_set))

    missing_by_col = list(zip(header, missing_counts))
    missing_by_col.sort(key=lambda x: x[1], reverse=True)

    return {
        "name": spec.name,
        "path": spec.path,
        "rows": rows,
        "columns": header,
        "min_dt": min_dt,
        "max_dt": max_dt,
        "unique_datetimes": unique_count,
        "duplicates": duplicates,
        "expected_hours": expected,
        "missing_hours": missing_time,
        "gap_segments": gap_segments,
        "max_gap_hours": max_gap_hours,
        "missing_by_col": missing_by_col,
        "parse_errors": parse_errors,
        "dt_set": dt_set,
    }


def _fmt_dt(dt: datetime | None) -> str:
    if dt is None:
        return "n/a"
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    results = [analyze_dataset(ds) for ds in DATASETS]
    sets = {r["name"]: r["dt_set"] for r in results}

    common_all = None
    for s in sets.values():
        common_all = s if common_all is None else common_all & s

    common_air_weather = sets.get("air_quality", set()) & sets.get("weather", set())
    base_count = len(common_air_weather)

    coverage = {}
    for name, s in sets.items():
        if base_count > 0:
            coverage[name] = len(common_air_weather & s) / base_count
        else:
            coverage[name] = 0.0

    out_path = Path("data/analysis/preprocessing/preprocess_report.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# Preprocessing Analysis Report")
    lines.append("")
    lines.append("## Dataset Overview")
    lines.append("")
    lines.append("| Dataset | Rows | Columns | Min Datetime | Max Datetime | Unique Datetimes | Duplicates | Parse Errors |")
    lines.append("|---|---:|---:|---|---|---:|---:|---:|")
    for r in results:
        lines.append(
            "| {name} | {rows} | {cols} | {min_dt} | {max_dt} | {unique} | {dup} | {pe} |".format(
                name=r["name"],
                rows=r["rows"],
                cols=len(r["columns"]),
                min_dt=_fmt_dt(r["min_dt"]),
                max_dt=_fmt_dt(r["max_dt"]),
                unique=r["unique_datetimes"],
                dup=r["duplicates"],
                pe=r["parse_errors"],
            )
        )

    lines.append("")
    lines.append("## Time Coverage & Gaps")
    lines.append("")
    lines.append("| Dataset | Expected Hours | Missing Hours | Gap Segments | Max Gap (hours) |")
    lines.append("|---|---:|---:|---:|---:|")
    for r in results:
        lines.append(
            "| {name} | {expected} | {missing} | {gaps} | {max_gap:.1f} |".format(
                name=r["name"],
                expected=r["expected_hours"] if r["expected_hours"] is not None else "n/a",
                missing=r["missing_hours"] if r["missing_hours"] is not None else "n/a",
                gaps=r["gap_segments"],
                max_gap=r["max_gap_hours"],
            )
        )

    lines.append("")
    lines.append("## Missing Values (Top 5 per Dataset)")
    lines.append("")
    for r in results:
        lines.append(f"### {r['name']}")
        lines.append("")
        top = r["missing_by_col"][:5]
        lines.append("| Column | Missing Count |")
        lines.append("|---|---:|")
        for col, count in top:
            lines.append(f"| {col} | {count} |")
        lines.append("")

    lines.append("## Alignment Between Sources")
    lines.append("")
    lines.append(f"- Common timestamps (air ∩ weather): {base_count}")
    lines.append(f"- Common timestamps (all sources): {len(common_all) if common_all is not None else 0}")
    lines.append("- Coverage vs air+weather base:")
    for name, ratio in coverage.items():
        lines.append(f"  - {name}: {ratio:.2%}")

    lines.append("")
    lines.append("## Key Findings")
    lines.append("")
    lines.append("- Time ranges are not fully aligned across sources (air/weather extend beyond holidays/traffic).")
    lines.append("- Missing values exist in multiple columns; see per-dataset tables above.")
    lines.append("- Hourly gaps and duplicate timestamps may affect merge consistency.")
    lines.append("")
    lines.append("## Recommended Preprocessing Actions")
    lines.append("")
    lines.append("1) Align time ranges across datasets before merge (clip to common window).")
    lines.append("2) Deduplicate by datetime after ingest (keep latest or aggregate).")
    lines.append("3) Impute or drop missing values per variable policy.")
    lines.append("4) Validate hourly continuity; fill gaps if needed for rolling/lag features.")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote report: {out_path}")


if __name__ == "__main__":
    main()
