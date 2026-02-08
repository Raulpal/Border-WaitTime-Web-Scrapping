import pandas as pd
import re
import numpy as np
from datetime import datetime

INPUT_XLSX = "elpaso_holiday_wait_times.xlsx"
OUTPUT_XLSX = "elpaso_holiday_wait_times_by_holiday_clean_sorted.xlsx"

META_COLS = ["Port", "Lane", "Sub-Lane", "Holiday", "Time"]

def safe_sheet_name(name: str) -> str:
    name = re.sub(r"[:\\/?*\[\]]", "_", str(name)).strip()
    return name[:31] if len(name) > 31 else name

def drop_all_blank_columns(df: pd.DataFrame) -> pd.DataFrame:
    tmp = df.copy()
    tmp = tmp.replace(r"^\s*$", np.nan, regex=True)
    keep = [c for c in tmp.columns if c in META_COLS or tmp[c].notna().any()]
    return df[keep]

def extract_date_from_header(col: str):
    """
    From: 'Monday, Dec 30, 2024 (min)' -> datetime.date(2024, 12, 30)
    Returns None if not parseable.
    """
    s = str(col)
    m = re.search(r"([A-Za-z]{3,}\s+\d{1,2},\s+\d{4})", s)
    if not m:
        return None
    date_str = m.group(1)
    for fmt in ("%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass
    return None

def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols = list(df.columns)

    meta = [c for c in META_COLS if c in cols]
    rest = [c for c in cols if c not in meta]

    # Sort rest by parsed date; unparseable columns go last (keeps stability)
    dated = []
    undated = []
    for c in rest:
        d = extract_date_from_header(c)
        if d is None:
            undated.append(c)
        else:
            dated.append((d, c))

    dated_sorted = [c for _, c in sorted(dated, key=lambda x: x[0])]

    return df[meta + dated_sorted + undated]

def main():
    df = pd.read_excel(INPUT_XLSX)

    if "Holiday" not in df.columns:
        raise ValueError("Expected a 'Holiday' column in the input file.")

    with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl") as writer:
        for holiday, block in df.groupby("Holiday", dropna=False):
            block_clean = drop_all_blank_columns(block)
            block_sorted = reorder_columns(block_clean)

            sheet = safe_sheet_name(holiday if pd.notna(holiday) else "UnknownHoliday")
            block_sorted.to_excel(writer, sheet_name=sheet, index=False)

    print(f"Saved: {OUTPUT_XLSX}")

if __name__ == "__main__":
    main()