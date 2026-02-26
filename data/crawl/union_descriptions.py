#!/usr/bin/env python3
"""Union all raw*_description.csv files into full_description.csv."""

import csv
from pathlib import Path


def main():
    crawl_dir = Path(__file__).parent
    def sort_key(p):
        s = p.stem  # e.g. "raw_description" or "raw2_description"
        if s == "raw_description":
            return 0
        num = s.replace("raw", "").replace("_description", "")
        return int(num) if num.isdigit() else 999

    files = sorted(crawl_dir.glob("raw*_description.csv"), key=sort_key)

    if not files:
        print("No raw*_description.csv files found")
        return

    all_rows = []
    header = None

    for f in files:
        with open(f, "r", encoding="utf-8-sig") as fp:
            reader = csv.reader(fp)
            rows = list(reader)
        if not rows:
            continue
        if header is None:
            header = rows[0]
        all_rows.extend(rows[1:])  # skip header

    # Renumber first column
    for i, row in enumerate(all_rows, start=1):
        if row:
            row[0] = str(i)

    out_path = crawl_dir / "full_description.csv"
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(all_rows)

    print(f"Union complete: {len(files)} files -> {out_path.name} ({len(all_rows)} rows)")


if __name__ == "__main__":
    main()
