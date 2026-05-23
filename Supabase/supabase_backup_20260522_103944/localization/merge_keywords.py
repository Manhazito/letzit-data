import csv, json, re

CSV_PATH = '/sessions/eager-beautiful-maxwell/mnt/localization/full_translation_review.csv'


def parse_keywords(pt_raw, en_raw):
    """
    Parse both keyword columns, merge, deduplicate (case-insensitive), and
    return a sorted-unique list preserving original casing of first occurrence.
    """
    terms = []

    # portuguese_keywords: JSON array  e.g. ["aipo","celery","aipo2"]
    if pt_raw.strip():
        try:
            parsed = json.loads(pt_raw)
            terms.extend(str(t).strip() for t in parsed if str(t).strip())
        except json.JSONDecodeError:
            # Fallback: treat as comma-separated
            terms.extend(t.strip().strip('"') for t in pt_raw.split(',') if t.strip())

    # english_keywords: comma-separated plain text  e.g. "celery, aipo"
    if en_raw.strip():
        terms.extend(t.strip() for t in en_raw.split(',') if t.strip())

    # Deduplicate: case-insensitive, keep first occurrence
    seen = set()
    unique = []
    for t in terms:
        key = t.lower()
        if key not in seen:
            seen.add(key)
            unique.append(t)

    return unique


def format_keywords(terms):
    """Format as [term1,term2,term3] — no quotes, no spaces after commas."""
    if not terms:
        return ''
    return '[' + ','.join(terms) + ']'


# ── Read ──────────────────────────────────────────────────────────────────────
with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    old_fields = list(reader.fieldnames)
    rows = list(reader)

# ── Build new fieldnames: replace pt_kw + en_kw with single 'keywords' ───────
new_fields = []
inserted = False
for col in old_fields:
    if col == 'portuguese_keywords':
        new_fields.append('keywords')   # insert merged column here
        inserted = True
    elif col == 'english_keywords':
        pass                             # drop this column
    else:
        new_fields.append(col)

# ── Transform rows ─────────────────────────────────────────────────────────────
changed = 0
for row in rows:
    merged = parse_keywords(row['portuguese_keywords'], row['english_keywords'])
    row['keywords'] = format_keywords(merged)
    if row['keywords'] != row['portuguese_keywords']:
        changed += 1

# ── Write ──────────────────────────────────────────────────────────────────────
with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=new_fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)

print(f"Rows processed : {len(rows)}")
print(f"Rows changed   : {changed}")
print(f"Old columns    : portuguese_keywords + english_keywords")
print(f"New column     : keywords")
print(f"File saved.")
