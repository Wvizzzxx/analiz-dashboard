# -*- coding: utf-8 -*-
import csv
import os

DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(DIR, "все данные с выгрузок")

def read_csv_tab(path):
    for enc in ["utf-16", "utf-16-le", "utf-16-be", "utf-8-sig", "cp1251", "latin-1"]:
        try:
            with open(path, "r", encoding=enc) as f:
                content = f.read()
            # Detect delimiter
            first_line = content.split("\n")[0]
            if "\t" in first_line:
                delimiter = "\t"
            else:
                delimiter = ","
            rows = list(csv.DictReader(content.splitlines(), delimiter=delimiter))
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

for name, fname in files.items():
    path = os.path.join(DATA_DIR, fname)
    rows = read_csv_tab(path)
    if not rows:
        print(f"{name}: FAILED TO READ")
        continue
    
    keys = list(rows[0].keys())
    print(f"\n{name}: {len(rows)} domains")
    print(f"  Keys: {keys}")
    
    # Find spam column
    spam_col = None
    for k in keys:
        if "spam" in k.lower():
            spam_col = k
            break
    
    if spam_col:
        spam_yes = 0
        spam_no = 0
        spam_other = 0
        for r in rows:
            val = str(r.get(spam_col, "")).strip().strip('"').lower()
            if val in ("yes", "true", "1"):
                spam_yes += 1
            elif val in ("no", "false", "0", ""):
                spam_no += 1
            else:
                spam_other += 1
        print(f"  Spam column: {spam_col}")
        print(f"  Is spam=YES: {spam_yes}")
        print(f"  Is spam=NO: {spam_no}")
        print(f"  Is spam=other: {spam_other}")
        if spam_yes > 0:
            # Show spam domains
            spam_domains = []
            for r in rows:
                val = str(r.get(spam_col, "")).strip().strip('"').lower()
                if val in ("yes", "true", "1"):
                    domain = str(r.get(keys[0], "")).strip().strip('"')
                    dr = str(r.get("DR", "?")).strip().strip('"')
                    spam_domains.append(f"    {domain} (DR={dr})")
            print(f"  Spam domains:")
            for d in spam_domains[:20]:
                print(d)
            if len(spam_domains) > 20:
                print(f"    ... and {len(spam_domains)-20} more")
    else:
        print(f"  No spam column found!")