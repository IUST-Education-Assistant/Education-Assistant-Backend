#!/usr/bin/env python3
"""
Create full_detail.csv from raw*.csv files (raw, raw2, ..., raw7).
Columns: page_url, image_url, name, rank, faculty
"""

import csv
from pathlib import Path


def find_column_indices(header: list[str], data_rows: list[list[str]]) -> dict[str, int]:
    """Find column indices by header name or content."""
    indices = {}

    # page_url: header contains "PAGE URL"
    for i, h in enumerate(header):
        if "PAGE URL" in h.upper():
            indices["page_url"] = i
            break

    # image_url: header is "Image" or starts with "Image"
    for i, h in enumerate(header):
        if h.strip().upper().startswith("IMAGE") and "URL" not in h.upper():
            indices["image_url"] = i
            break

    # name: header contains "Description"
    for i, h in enumerate(header):
        if "Description" in h and "Align" not in h:
            indices["name"] = i
            break

    # rank: Align-middle column with values like دانشیار, استاد, استاديار
    rank_markers = ["دانشيار", "دانشیار", "استاد", "استاديار", "نا مشخص"]
    for col_idx in range(len(header)):
        if "Align" not in header[col_idx]:
            continue
        for row in data_rows[:30]:
            if col_idx < len(row) and any(m in row[col_idx] for m in rank_markers):
                if len(row[col_idx].strip()) < 20:  # rank is short
                    indices["rank"] = col_idx
                    break
        if "rank" in indices:
            break

    # faculty: column with دانشکده (faculty names like دانشکده مهندسي برق)
    for col_idx in range(len(header)):
        for row in data_rows[:30]:
            if col_idx < len(row) and "دانشکده" in row[col_idx]:
                indices["faculty"] = col_idx
                break
        if "faculty" in indices:
            break

    return indices


def main():
    crawl_dir = Path(__file__).parent

    def sort_key(p):
        s = p.stem
        if s == "raw":
            return 0
        num = s.replace("raw", "")
        return int(num) if num.isdigit() else 999

    files = sorted(
        [f for f in crawl_dir.glob("raw*.csv") if "_description" not in f.name],
        key=lambda p: sort_key(p),
    )

    if not files:
        print("No raw*.csv files found (excluding *_description)")
        return

    all_rows = []
    for f in files:
        with open(f, "r", encoding="utf-8-sig") as fp:
            reader = csv.reader(fp)
            rows = list(reader)
        if len(rows) < 2:
            continue
        header = rows[0]
        data_rows = rows[1:]
        indices = find_column_indices(header, data_rows)

        for row in data_rows:
            out = {
                "page_url": row[indices["page_url"]] if "page_url" in indices and indices["page_url"] < len(row) else "",
                "image_url": row[indices["image_url"]] if "image_url" in indices and indices["image_url"] < len(row) else "",
                "name": row[indices["name"]] if "name" in indices and indices["name"] < len(row) else "",
                "rank": row[indices["rank"]] if "rank" in indices and indices["rank"] < len(row) else "",
                "faculty": row[indices["faculty"]] if "faculty" in indices and indices["faculty"] < len(row) else "",
            }
            all_rows.append([out["page_url"], out["image_url"], out["name"], out["rank"], out["faculty"]])

    out_path = crawl_dir / "full_detail.csv"
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["page_url", "image_url", "name", "rank", "faculty"])
        writer.writerows(all_rows)

    print(f"Created {out_path.name} ({len(all_rows)} rows)")


if __name__ == "__main__":
    main()
