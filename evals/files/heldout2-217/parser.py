import csv


def parse(path):
    """Read a CSV of name,score rows and return a list of (name, int score)."""
    with open(path, newline="", encoding="utf-8") as f:
        return [(row["name"], int(row["score"])) for row in csv.DictReader(f)]


def legacy_parse(path):
    """Old fixed-width reader from before the CSV export. No longer used."""
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            name = line[:20].strip()
            score = int(line[20:].strip())
            rows.append((name, score))
    return rows


def top(rows, n=3):
    return sorted(rows, key=lambda r: r[1], reverse=True)[:n]
