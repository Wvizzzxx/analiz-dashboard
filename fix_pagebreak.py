# -*- coding: utf-8 -*-
import os

DIR = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(DIR, "Анализ_ссылочной_массы_дашборд.html")

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add page-break-before to priority item 3
old = '<div class="priority-item">\n                    <div class="priority-num">3</div>'
new = '<div class="priority-item" style="page-break-before:always;">\n                    <div class="priority-num">3</div>'
content = content.replace(old, new)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done: page-break-before added to priority item 3")