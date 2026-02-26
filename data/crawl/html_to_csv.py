#!/usr/bin/env python3
"""
Scan HTML files in the crawl directory and export table data to CSV.
Each HTML file gets a corresponding CSV in the same directory.
Uses only Python standard library.
"""

import csv
import re
from html.parser import HTMLParser
from pathlib import Path

# Regex to remove emoji and similar symbols (covers common Unicode emoji ranges)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001F9FF"  # Misc Symbols, Pictographs, Emoticons
    "\U00002600-\U000026FF"  # Misc symbols (☀☁☂...)
    "\U00002700-\U000027BF"  # Dingbats (✂✏...)
    "\U0001F600-\U0001F64F"  # Emoticons
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols
    "\U0000FE00-\U0000FE0F"  # Variation Selectors
    "\U0001F1E0-\U0001F1FF"  # Flags
    "]+",
    flags=re.UNICODE,
)


def strip_emoji(text: str) -> str:
    """Remove emoji and variation selectors from text."""
    return EMOJI_PATTERN.sub("", text)


class TableParser(HTMLParser):
    """Extract table rows (list of cell texts) from HTML."""

    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = []
        self.current_row = []
        self.current_cell = []
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.cell_tag = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
            self.current_table = []
        elif self.in_table and tag == "tr":
            self.in_row = True
            self.current_row = []
        elif self.in_row and tag in ("td", "th"):
            self.in_cell = True
            self.cell_tag = tag
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


def parse_html_tables(html_path: Path) -> list[list[list[str]]]:
    """
    Parse all tables from an HTML file.
    Returns a list of tables, each table is a list of rows, each row is a list of cell strings.
    """
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    parser = TableParser()
    parser.feed(content)
    return parser.tables


def export_to_csv(tables_data: list[list[list[str]]], csv_path: Path) -> None:
    """Export table data to CSV. Uses the largest table if multiple exist."""
    if not tables_data:
        return

    rows = max(tables_data, key=len)
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def main():
    crawl_dir = Path(__file__).parent
    html_files = sorted(crawl_dir.glob("*.html"))

    if not html_files:
        print(f"No HTML files found in {crawl_dir}")
        return

    for html_path in html_files:
        try:
            tables_data = parse_html_tables(html_path)
            if not tables_data:
                print(f"  No tables found in {html_path.name}")
                continue

            csv_path = html_path.with_suffix(".csv")
            export_to_csv(tables_data, csv_path)
            row_count = sum(len(t) for t in tables_data)
            print(f"  Exported {html_path.name} -> {csv_path.name} ({row_count} rows)")
        except Exception as e:
            print(f"  Error processing {html_path.name}: {e}")

    print("Done.")


if __name__ == "__main__":
    main()
