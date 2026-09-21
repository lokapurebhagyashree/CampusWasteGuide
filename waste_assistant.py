"""
Campus Waste Guide Assistant
Loads all rules dynamically from knowledge_base.txt — always in sync.
"""

import re
import os


KB_FILE = os.path.join(os.path.dirname(__file__), "knowledge_base.txt")


def load_knowledge_base(filepath):
    """Parse knowledge_base.txt and return {item_keyword: bin_name}."""
    kb = {}
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Match lines like: "42. Banana peel → Green Compost Bin"
            m = re.match(r"^\d+\.\s+(.+?)\s+→\s+(.+)$", line)
            if m:
                item = m.group(1).strip().lower()
                # Strip parenthetical qualifiers for broader matching
                item_clean = re.sub(r"\s*\(.*?\)", "", item).strip()
                bin_name = m.group(2).strip()
                kb[item_clean] = bin_name
                if item_clean != item:
                    kb[item] = bin_name  # also keep full form
    return kb


def find_bin(user_input, kb):
    """Return bin name if a keyword matches user input, else None."""
    query = user_input.strip().lower()
    # 1. Exact match
    if query in kb:
        return kb[query]
    # 2. Keyword contained in query OR query contained in keyword
    for keyword, bin_name in kb.items():
        if keyword in query or query in keyword:
            return bin_name
    return None


def main():
    try:
        kb = load_knowledge_base(KB_FILE)
    except FileNotFoundError:
        print(f"ERROR: Could not find {KB_FILE}")
        return

    total = len(set(kb.values()) and kb)
    print("♻️  Campus Waste Guide Assistant")
    print(f"   Knowledge base loaded: {len(kb)} entries across 5 bins")
    print("   Type 'quit' to exit.\n")

    while True:
        user_input = input("What item are you disposing? ").strip()

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Goodbye! Dispose responsibly! 🌱")
            break

        bin_name = find_bin(user_input, kb)

        if bin_name:
            print(f"✅ Please dispose of that in the {bin_name}.\n")
        else:
            print("❓ I'm not sure. Please check the bin labels.\n")


if __name__ == "__main__":
    main()
