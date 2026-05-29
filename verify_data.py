# -*- coding: utf-8 -*-
import csv
import os

DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(DIR, "все данные с выгрузок")

def read_csv(path):
    for enc in ["utf-16", "utf-16-le", "utf-16-be", "utf-8-sig", "cp1251", "latin-1"]:
        try:
            with open(path, "r", encoding=enc) as f:
                content = f.read()
            rows = list(csv.DictReader(content.splitlines()))
            return rows
        except:
            continue
    return []

files = {
    "LSR": "referring domains1-www.lsr.csv",
    "PIK": "pik.ru-refdomains1.csv",
    "Etalon": "etalongroup.ru-refdomains1.csv",
    "Samolet": "samolet.ru-refdomains1.csv",
    "Setl": "setlgroup.ru-refdomains1.csv",
}

print("=== REFERRING DOMAINS ===")
for name, fname in files.items():
    path = os.path.join(DATA_DIR, fname)
    rows = read_csv(path)
    print(f"\n{name}: {len(rows)} referring domains")
    if rows:
        keys = list(rows[0].keys())
        print(f"  Columns: {keys[:10]}")
        dr_col = None
        for k in keys:
            if "DR" in k:
                dr_col = k
                break
        if dr_col:
            drs = []
            for r in rows:
                try:
                    drs.append(int(r[dr_col]))
                except:
                    pass
            if drs:
                drs_sorted = sorted(drs)
                n = len(drs)
                print(f"  DR column: {dr_col}")
                print(f"  Count: {n}, Avg: {sum(drs)/n:.1f}, Median: {drs_sorted[n//2]}")
                print(f"  DR >= 70: {sum(1 for d in drs if d >= 70)}")
                print(f"  DR >= 50: {sum(1 for d in drs if d >= 50)}")

print("\n\n=== SPAM ANALYSIS ===")
for name, fname in files.items():
    path = os.path.join(DATA_DIR, fname)
    rows = read_csv(path)
    if rows:
        keys = list(rows[0].keys())
        spam_col = None
        for k in keys:
            if "spam" in k.lower() or "Spam" in k:
                spam_col = k
                break
        if spam_col:
            spam_count = 0
            for r in rows:
                val = str(r.get(spam_col, "")).strip()
                if val.lower() in ("yes", "true", "1", "da"):
                    spam_count += 1
            print(f"{name}: spam={spam_count} out of {len(rows)} ({spam_count*100//len(rows)}%)")
        else:
            print(f"{name}: no spam column found")
            print(f"  Columns: {keys}")

print("\n\n=== BACKLINKS ===")
bl_files = {
    "LSR": "backlinks1-www.lsr.csv",
    "PIK": "backlinks_pik.ru1.csv",
    "Etalon": "etalongroup.ru-backlinks1.csv",
    "Samolet": "samolet.ru-backlinks1.csv",
    "Setl": "setlgroup.ru-refdomains1.csv",
}
for name, fname in bl_files.items():
    path = os.path.join(DATA_DIR, fname)
    rows = read_csv(path)
    print(f"{name}: {len(rows)} backlinks")
