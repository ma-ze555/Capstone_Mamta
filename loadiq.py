"""
LoadIQ - Priority-Driven Delivery Load Optimisation Engine (CP-048)
Simple console app. Greedy rule: highest priority parcels are loaded first.
Priority: 1 = High, 2 = Medium, 3 = Low
"""

PRIORITY_NAMES = {1: "High", 2: "Medium", 3: "Low"}

parcels = []   # each: {"id", "weight", "volume", "priority"}
vans = []      # each: {"id", "max_w", "max_v", "load_w", "load_v", "parcels"}
unloaded = []  # each: {"parcel", "reason"}


# ---------- input helpers (all validation lives here) ----------
def ask_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Error: this cannot be empty.")


def ask_number(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("  Error: enter a number, e.g. 12.5")
            continue
        if value <= 0:
            print("  Error: value must be greater than 0.")
            continue
        return value


def ask_priority():
    while True:
        raw = input("  Priority (1=High, 2=Medium, 3=Low): ").strip()
        if raw in ("1", "2", "3"):
            return int(raw)
        print("  Error: priority must be 1, 2 or 3.")


def id_exists(items, item_id):
    return any(item["id"].lower() == item_id.lower() for item in items)


# ---------- core features ----------
def add_parcel():
    print("\n--- Add Parcel ---")
    pid = ask_text("  Parcel ID: ")
    if id_exists(parcels, pid):
        print("  Error: parcel ID already exists.")
        return
    weight = ask_number("  Weight (kg): ")
    volume = ask_number("  Volume (m3): ")
    priority = ask_priority()
    parcels.append({"id": pid, "weight": weight, "volume": volume, "priority": priority})
    print(f"  Parcel {pid} saved.")


def add_van():
    print("\n--- Add Van ---")
    vid = ask_text("  Van ID: ")
    if id_exists(vans, vid):
        print("  Error: van ID already exists.")
        return
    max_w = ask_number("  Weight capacity (kg): ")
    max_v = ask_number("  Volume capacity (m3): ")
    vans.append({"id": vid, "max_w": max_w, "max_v": max_v,
                 "load_w": 0.0, "load_v": 0.0, "parcels": []})
    print(f"  Van {vid} saved.")


def view_data():
    print("\n--- Parcels ---")
    if not parcels:
        print("  (none)")
    for p in parcels:
        print(f"  {p['id']:<8} {p['weight']:>7.1f} kg {p['volume']:>6.2f} m3  "
              f"{PRIORITY_NAMES[p['priority']]}")
    print("--- Vans ---")
    if not vans:
        print("  (none)")
    for v in vans:
        print(f"  {v['id']:<8} max {v['max_w']:.1f} kg, {v['max_v']:.2f} m3")


def assign_parcels():
    """Greedy: sort by priority (then heavier first), put each in the first van that fits."""
    if not parcels or not vans:
        print("  Error: add at least one parcel and one van first.")
        return

    # reset any earlier run
    unloaded.clear()
    for v in vans:
        v["load_w"], v["load_v"], v["parcels"] = 0.0, 0.0, []

    order = sorted(parcels, key=lambda p: (p["priority"], -p["weight"]))
    biggest_w = max(v["max_w"] for v in vans)
    biggest_v = max(v["max_v"] for v in vans)

    for p in order:
        placed = False
        for v in vans:
            if (v["load_w"] + p["weight"] <= v["max_w"]
                    and v["load_v"] + p["volume"] <= v["max_v"]):
                v["parcels"].append(p)
                v["load_w"] += p["weight"]
                v["load_v"] += p["volume"]
                placed = True
                break
        if not placed:
            if p["weight"] > biggest_w:
                reason = "Heavier than the biggest van"
            elif p["volume"] > biggest_v:
                reason = "Bigger than the biggest van"
            else:
                reason = "No van has enough space left"
            unloaded.append({"parcel": p, "reason": reason})

    print(f"  Done. Loaded {len(parcels) - len(unloaded)} parcel(s), "
          f"left behind {len(unloaded)}.")


def print_load_sheet():
    print("\n========== LOAD SHEET ==========")
    if not any(v["parcels"] for v in vans):
        print("  Nothing loaded yet. Run option 4 first.")
        return
    for v in vans:
        print(f"\nVan {v['id']}")
        if not v["parcels"]:
            print("  (empty)")
        for p in v["parcels"]:
            print(f"  {p['id']:<8} {p['weight']:>7.1f} kg {p['volume']:>6.2f} m3  "
                  f"{PRIORITY_NAMES[p['priority']]}")
        print(f"  Weight used: {v['load_w']:.1f} / {v['max_w']:.1f} kg "
              f"({v['load_w'] / v['max_w'] * 100:.0f}%)")
        print(f"  Volume used: {v['load_v']:.2f} / {v['max_v']:.2f} m3 "
              f"({v['load_v'] / v['max_v'] * 100:.0f}%)")


def print_unloaded():
    print("\n--- Parcels NOT loaded ---")
    if not unloaded:
        print("  None. Every parcel was loaded (or run option 4 first).")
        return
    for item in unloaded:
        p = item["parcel"]
        print(f"  {p['id']:<8} {PRIORITY_NAMES[p['priority']]:<7} -> {item['reason']}")


def load_sample_data():
    parcels.clear()
    vans.clear()
    unloaded.clear()
    for pid, w, vol, pr in [("P1", 40, 0.5, 1), ("P2", 120, 1.5, 3), ("P3", 60, 0.8, 1),
                            ("P4", 90, 1.0, 2), ("P5", 500, 3.0, 2), ("P6", 30, 0.4, 3)]:
        parcels.append({"id": pid, "weight": w, "volume": vol, "priority": pr})
    for vid, mw, mv in [("VAN-A", 200, 3.0), ("VAN-B", 150, 2.0)]:
        vans.append({"id": vid, "max_w": mw, "max_v": mv,
                     "load_w": 0.0, "load_v": 0.0, "parcels": []})
    print("  Sample data loaded (6 parcels, 2 vans).")


# ---------- menu ----------
def main():
    print("=== LoadIQ: Delivery Load Optimiser ===")
    while True:
        print("\n1. Add parcel\n2. Add van\n3. View parcels & vans\n"
              "4. Assign parcels to vans\n5. Print load sheet\n"
              "6. Show parcels not loaded\n7. Load sample data\n0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_parcel()
        elif choice == "2":
            add_van()
        elif choice == "3":
            view_data()
        elif choice == "4":
            assign_parcels()
        elif choice == "5":
            print_load_sheet()
        elif choice == "6":
            print_unloaded()
        elif choice == "7":
            load_sample_data()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("  Error: choose a number from the menu.")


if __name__ == "__main__":
    main()
