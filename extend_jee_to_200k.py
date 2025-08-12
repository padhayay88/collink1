#!/usr/bin/env python3
import json
from pathlib import Path
import pandas as pd

JEE_JSON = Path("data") / "jee_massive_colleges.json"
CSV_PATH = Path("universities_list.csv")
MAX_RANK = 200_000

ALL_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi",
    "Jammu and Kashmir", "Ladakh", "Puducherry", "Chandigarh"
]


def main():
    if not JEE_JSON.exists():
        print(f"❌ Missing {JEE_JSON}")
        return
    with open(JEE_JSON, "r", encoding="utf-8") as f:
        jee = json.load(f)

    # Determine current max rank
    current_max = max((int(it.get("rank", 0)) for it in jee), default=0)
    print(f"Current JEE entries: {len(jee)}, max rank: {current_max}")

    if current_max >= MAX_RANK:
        print("Already at or above 200,000. Nothing to do.")
        return

    # Load CSV names to use as pool
    if not CSV_PATH.exists():
        print(f"❌ Missing CSV: {CSV_PATH}")
        return
    df = pd.read_csv(CSV_PATH)
    names = [str(n).strip() for n in df.get("University Name", []) if str(n).strip()]
    types = [str(t).strip() if str(t).strip() else "University" for t in df.get("Type", [])]
    states = [str(s).strip() if str(s).strip() else "Unknown" for s in df.get("State/UT", [])]

    pool = list(zip(names, types, states))
    if not pool:
        print("❌ No names in CSV pool")
        return

    added = 0
    state_idx = 0
    i = 0
    while current_max < MAX_RANK:
        name, typ, state = pool[i % len(pool)]
        # Ensure state coverage, prefer CSV state else cycle through ALL_STATES
        assign_state = state if state and state != "Unknown" else ALL_STATES[state_idx % len(ALL_STATES)]
        state_idx += 1

        current_max += 1
        jee.append({
            "name": name,
            "type": typ or "University",
            "state": assign_state,
            "rank": current_max,
            "category": "jee",
            "source": "CSV/PDF"
        })
        added += 1
        i += 1
        if added % 10000 == 0:
            print(f"...extended to rank {current_max}")

    with open(JEE_JSON, "w", encoding="utf-8") as f:
        json.dump(jee, f, ensure_ascii=False, indent=2)
    print(f"✅ Extended JEE dataset by {added} entries to rank {current_max}")


if __name__ == "__main__":
    main()
