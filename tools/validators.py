# tools/validators.py
"""Simple validators for SPL detections used by unit tests."""

import re

# --- regexes ---
INDEX_RE = re.compile(r'(?<!\w)index\s*=\s*([^\s|]+)', re.IGNORECASE)
TABLE_RE = re.compile(r'(?<!\w)table\s+', re.IGNORECASE)
STATS_RE = re.compile(r'(?<!\w)(?:stats|tstats)\s+', re.IGNORECASE)
MACRO_CALL_RE = re.compile(r'`([a-zA-Z0-9:_-]+)`')

# --- SPL checks expected by tests ---
def has_index(spl: str) -> bool:
    return bool(spl and INDEX_RE.search(spl))

def has_table(spl: str) -> bool:
    return bool(spl and TABLE_RE.search(spl))

def has_stats(spl: str) -> bool:
    return bool(spl and STATS_RE.search(spl))

def macro_calls(spl: str):
    if not spl:
        return []
    return MACRO_CALL_RE.findall(spl)

# --- metadata checks expected by tests ---
def has_any_macro_field(detection: dict) -> bool:
    m = detection.get("macros", [])
    return bool(m)

def has_ttp(detection: dict) -> bool:
    tags = detection.get("tags", {}) or {}
    # allow either key
    ttps = tags.get("mitre_attack") or tags.get("mitre_attack_id") or tags.get("mitre") or []
    return bool(ttps)

def has_testing_data(detection: dict) -> bool:
    t = detection.get("testing")
    if not t:
        return False
    return bool(t.get("dataset_hint") or t.get("sample_events"))
