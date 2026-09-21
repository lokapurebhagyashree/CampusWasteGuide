"""
Analysis script for knowledge_base.txt
Checks:
  1. File structure and item count per category
  2. Duplicate items
  3. Numbering continuity
  4. Items missing from waste_assistant.py
  5. Simulated query tests across all 5 bins
"""

import re

KB_FILE = "knowledge_base.txt"

# ── 1. Parse knowledge_base.txt ──────────────────────────────────────────────
categories = {}
current_cat = None
current_bin = None
all_items = []          # list of (number, item_name, bin_name)
number_sequence = []

with open(KB_FILE, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line == "Waste Segregation Rules":
            continue
        # Category header
        if line.startswith("---"):
            m = re.search(r"→\s+(.+?)\s+---", line)
            if m:
                current_bin = m.group(1).strip()
                current_cat = current_bin
                categories[current_cat] = []
            continue
        # Item line: "123. Item name → Bin name"
        m = re.match(r"^(\d+)\.\s+(.+?)\s+→\s+(.+)$", line)
        if m:
            num = int(m.group(1))
            item = m.group(2).strip()
            bin_name = m.group(3).strip()
            all_items.append((num, item, bin_name))
            number_sequence.append(num)
            if current_cat:
                categories[current_cat].append((num, item))

# ── 2. Load assistant knowledge base dynamically (same as waste_assistant.py) ─
import sys
sys.path.insert(0, ".")
from waste_assistant import load_knowledge_base, find_bin

assistant_kb = load_knowledge_base(KB_FILE)

def find_bin_assistant(item):
    return find_bin(item, assistant_kb)

# ── 3. Print report ──────────────────────────────────────────────────────────
SEP = "─" * 60

print(SEP)
print("  KNOWLEDGE BASE ANALYSIS REPORT")
print(SEP)

# 3a. Item count per category
print("\n📊 ITEM COUNT PER CATEGORY")
total = 0
for cat, items in categories.items():
    print(f"  {cat:<40} {len(items):>3} items")
    total += len(items)
print(f"  {'TOTAL':<40} {total:>3} items")

# 3b. Numbering check
print("\n🔢 NUMBERING CONTINUITY")
expected = list(range(1, total + 1))
if number_sequence == expected:
    print(f"  ✅ Numbering is continuous from 1 to {total} — no gaps or duplicates")
else:
    missing = sorted(set(expected) - set(number_sequence))
    dupes   = sorted(n for n in number_sequence if number_sequence.count(n) > 1)
    if missing: print(f"  ❌ Missing numbers: {missing}")
    if dupes:   print(f"  ❌ Duplicate numbers: {list(set(dupes))}")

# 3c. Duplicate item names
print("\n🔍 DUPLICATE ITEM NAMES")
names = [i[1].lower() for i in all_items]
seen = set()
dupes_found = []
for n in names:
    if n in seen:
        dupes_found.append(n)
    seen.add(n)
if dupes_found:
    print(f"  ⚠️  Duplicates found: {dupes_found}")
else:
    print(f"  ✅ No duplicate item names found")

# 3d. Coverage gap: assistant vs knowledge_base
print("\n⚠️  COVERAGE GAP — items in knowledge_base.txt NOT in waste_assistant.py")
missing_from_assistant = []
for _, item, bin_name in all_items:
    result = find_bin_assistant(item)
    if result != bin_name:
        missing_from_assistant.append((item, bin_name, result))

print(f"  knowledge_base.txt : {total} items")
print(f"  waste_assistant.py : {len(assistant_kb)} items")
print(f"  Unmatched items    : {len(missing_from_assistant)}")
if missing_from_assistant:
    print(f"\n  First 10 unmatched examples:")
    for item, expected_bin, got in missing_from_assistant[:10]:
        got_str = got if got else "❓ fallback"
        print(f"    '{item}' → expected: {expected_bin} | got: {got_str}")

# 3e. Simulated query tests
print("\n🧪 SIMULATED QUERY TESTS (against waste_assistant.py)")
test_cases = [
    ("glass bottle",           "Blue Recycling Bin"),
    ("old newspaper",          "Blue Recycling Bin"),
    ("banana peel",            "Green Compost Bin"),
    ("leftover rice",          "Green Compost Bin"),
    ("chips packet",           "Black General Waste"),
    ("styrofoam cup",          "Black General Waste"),
    ("old laptop",             "Admin Office E-Waste Drop-off"),
    ("mobile phone",           "Admin Office E-Waste Drop-off"),
    ("used tissue",            "Red Sanitary Waste Bin"),
    ("sanitary pad",           "Red Sanitary Waste Bin"),
    ("broken umbrella",        None),   # should be Black General Waste in KB but unknown to assistant
    ("smart watch",            None),   # E-Waste in KB but unknown to assistant
]

passed = 0
failed = 0
for query, expected in test_cases:
    result = find_bin_assistant(query)
    if expected is None:
        status = "⚠️  FALLBACK" if result is None else f"⚠️  GOT: {result}"
    elif result == expected:
        status = "✅ PASS"
        passed += 1
    else:
        status = f"❌ FAIL  (got: {result if result else 'fallback'})"
        failed += 1
    print(f"  {status:<30} '{query}'  →  expected: {expected if expected else 'fallback'}")

print(f"\n  Results: {passed} passed, {failed} failed, {len(test_cases)-passed-failed} warnings")

print(f"\n{SEP}")
print("  CONCLUSION")
print(SEP)
if len(missing_from_assistant) > 0:
    print(f"  ❌ waste_assistant.py is OUT OF SYNC with knowledge_base.txt")
    print(f"     {len(missing_from_assistant)} of {total} items are NOT covered by the assistant.")
    print(f"     ACTION REQUIRED: Rebuild waste_assistant.py from knowledge_base.txt")
else:
    print(f"  ✅ waste_assistant.py fully covers all {total} items in knowledge_base.txt")
print(SEP)
