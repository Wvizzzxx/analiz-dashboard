# -*- coding: utf-8 -*-
import re, os

DIR = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(DIR, "Анализ_ссылочной_массы_дашборд.html")

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove PDF export bar
content = re.sub(r'<!-- PDF EXPORT BUTTON -->.*?</div>\s*\n', '', content, flags=re.DOTALL)

# Remove html2pdf.js script tag
content = re.sub(r'<!-- html2pdf\.js library -->.*?</script>\s*\n', '', content, flags=re.DOTALL)

# Remove exportPDF function script
content = re.sub(r'<script>\s*function exportPDF\(\).*?</script>', '', content, flags=re.DOTALL)

# Remove PDF-related CSS
content = re.sub(r'/\* PDF Export Button \*/.*?@keyframes spin \{.*?\}', '', content, flags=re.DOTALL)

# Remove print-hide for PDF bar
content = re.sub(r'\.pdf-export-bar \{ display: none !important; \}\s*', '', content)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done: PDF button and related code removed")