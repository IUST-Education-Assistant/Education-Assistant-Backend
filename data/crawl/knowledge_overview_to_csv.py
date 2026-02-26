#!/usr/bin/env python3
"""
Extract knowledge_overview(active).html to CSV with English column names.
Column order (left to right):
  استناد بازای مقاله -> citation_per_article
  مستندات -> documents
  رتبه علمی -> academic_rank
  دانشکده -> faculty
  نام -> name
  URL -> url
  [rank - dropped]
  [دانشکده duplicate - dropped]
  link -> url (URL dropped, link kept and renamed)
  G-Index -> g_index
  H-Index -> h_index
  [row - dropped]
"""

import csv
import re
from html.parser import HTMLParser
from pathlib import Path

# Regex to remove emoji
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001F9FF"
    "\U00002600-\U000026FF"
    "\U00002700-\U000027BF"
    "\U0001F600-\U0001F64F"
    "\U0001F900-\U0001F9FF"
    "\U0000FE00-\U0000FE0F"
    "\U0001F1E0-\U0001F1FF"
    "]+",
    flags=re.UNICODE,
)


def strip_emoji(text: str) -> str:
    return EMOJI_PATTERN.sub("", text)


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = []
        self.current_row = []
        self.current_cell = []
        self.in_table = False
        self.in_row = False
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
            self.current_table = []
        elif self.in_table and tag == "tr":
            self.in_row = True
            self.current_row = []
        elif self.in_row and tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = []

    def handle_endtag(self, tag):
        if tag == "table":
            if self.current_table:
                self.tables.append(self.current_table)
            self.in_table = False
        elif tag == "tr":
            if self.current_row:
                self.current_table.append(self.current_row)
            self.in_row = False
        elif tag in ("td", "th") and self.in_cell:
            text = " ".join("".join(self.current_cell).split())
            text = strip_emoji(text)
            self.current_row.append(text)
            self.in_cell = False

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell.append(data)


# Column mapping: source index -> output column name
# Source: 0=#, 1=citation_per_article, 2=documents, 3=academic_rank, 4=faculty,
# 5=name, 6=link(keep as url), 7=rank, 8=faculty_dup(drop), 9=url(drop),
# 10=g_index, 11=h_index, 12=citations, 13=i10_index
COLUMN_MAP = [
    (1, "citation_per_article"),   # استناد بازای مقاله
    (2, "documents"),              # مستندات
    (3, "academic_rank"),          # رتبه علمی
    (4, "faculty"),                # دانشکده
    (5, "name"),                  # نام
    (6, "url"),                   # link -> url (profile URL)
    (10, "g_index"),              # G-Index
    (11, "h_index"),             # H-Index
]


def parse_html(html_path: Path) -> list[list[list[str]]]:
    with open(html_path, "r", encoding="utf-8") as f:
        parser = TableParser()
        parser.feed(f.read())
    return parser.tables


def main():
    crawl_dir = Path(__file__).parent
    html_path = crawl_dir / "knowledge_overview(active).html"
    csv_path = crawl_dir / "knowledge_overview(active).csv"

    if not html_path.exists():
        print(f"File not found: {html_path}")
        return

    tables = parse_html(html_path)
    if not tables:
        print("No tables found")
        return

    rows = max(tables, key=len)
    header = [name for _, name in COLUMN_MAP]
    output_rows = [header]

    for data_row in rows[1:]:  # skip original header
        out_row = []
        for src_idx, _ in COLUMN_MAP:
            val = data_row[src_idx] if src_idx < len(data_row) else ""
            out_row.append(val)
        output_rows.append(out_row)

    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(output_rows)

    print(f"Exported {csv_path.name} ({len(output_rows) - 1} rows)")


if __name__ == "__main__":
    main()
