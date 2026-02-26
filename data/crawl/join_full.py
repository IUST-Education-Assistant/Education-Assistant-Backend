#!/usr/bin/env python3
"""
Join full_description and full_detail by page_url/URL.
Output: page_url, image_url, name, rank, faculty, content, word_count
Drops: title, description
"""

import csv
from pathlib import Path


def main():
    crawl_dir = Path(__file__).parent

    # Load full_detail (page_url as key)
    detail_rows = {}
    with open(crawl_dir / "full_detail.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            detail_rows[row["page_url"].strip()] = row

    # Load full_description, join on URL
    # full_description: #↑, URL⋮, Title⋮, Description⋮, Content⋮, Word Count⋮
    desc_headers = None
    url_col = None
    content_col = None
    word_count_col = None
    title_col = None
    desc_col = None

    joined = []
    with open(crawl_dir / "full_description.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        headers = next(reader)
        # Find column indices
        for i, h in enumerate(headers):
            h_clean = h.strip().replace("⋮", "")
            if "URL" in h_clean and "PAGE" not in h_clean.upper():
                url_col = i
            elif "Content" in h_clean:
                content_col = i
            elif "Word Count" in h_clean:
                word_count_col = i
            elif "Title" in h_clean:
                title_col = i
            elif "Description" in h_clean:
                desc_col = i

        for row in reader:
            if url_col is None or url_col >= len(row):
                continue
            url = row[url_col].strip()
            if url not in detail_rows:
                continue
            detail = detail_rows[url]
            content = row[content_col] if content_col is not None and content_col < len(row) else ""
            word_count = row[word_count_col] if word_count_col is not None and word_count_col < len(row) else ""
            joined.append({
                "page_url": url,
                "image_url": detail.get("image_url", ""),
                "name": detail.get("name", ""),
                "rank": detail.get("rank", ""),
                "faculty": detail.get("faculty", ""),
                "content": content,
                "word_count": word_count,
            })

    out_path = crawl_dir / "full_joined.csv"
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["page_url", "image_url", "name", "rank", "faculty", "content", "word_count"])
        writer.writeheader()
        writer.writerows(joined)

    print(f"Created {out_path.name} ({len(joined)} rows)")


if __name__ == "__main__":
    main()
