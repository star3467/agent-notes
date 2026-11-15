#!/usr/bin/env python3
"""檢查 pages/ 下的頁面是否遵守 CLAUDE.md 的規則。用法：python3 scripts/check.py
全部通過回傳 0，有錯誤回傳 1。只用標準函式庫。"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.html$")
errors = []

def err(f, msg):
    errors.append(f"{f}: {msg}")

index = (ROOT / "index.html").read_text(encoding="utf-8")
SECTIONS = {"概念": "CONCEPTS", "模式": "PATTERNS"}   # tag -> index.html 標記名稱
listed = {}
for tag, mark in SECTIONS.items():
    m = re.search(rf"<!-- {mark}:START -->(.*?)<!-- {mark}:END -->", index, re.S)
    if not m:
        err("index.html", f"找不到 <!-- {mark}:START --> ... <!-- {mark}:END --> 標記")
    listed[tag] = set(re.findall(r'href="pages/([^"]+)"', m.group(1))) if m else set()
all_index_links = set(re.findall(r'href="pages/([^"]+)"', index))
EXEMPT_FROM_SECTIONS = {"agent-patterns.html"}   # 首頁「從這裡開始」的總覽頁

pages = sorted((ROOT / "pages").glob("*.html"))
if not pages:
    err("pages/", "沒有任何頁面")

for p in pages:
    name, text = p.name, p.read_text(encoding="utf-8")
    if not KEBAB.match(name):
        err(name, "檔名必須是小寫英文與連字號（kebab-case）")
    if '<html lang="zh-Hant">' not in text:
        err(name, '缺少 <html lang="zh-Hant">')
    if len(re.findall(r"<h1[ >]", text)) != 1:
        err(name, "必須恰好一個 <h1>")
    t = re.search(r"<title>(.*?)</title>", text)
    if not t or not t.group(1).endswith(" | AI Agent 學習筆記"):
        err(name, "<title> 必須以「 | AI Agent 學習筆記」結尾")
    if not re.search(r'<meta name="description" content="[^"]{10,}"', text):
        err(name, "缺少 meta description（至少 10 字）")
    if 'href="../assets/style.css"' not in text:
        err(name, "必須引用 ../assets/style.css")
    if "<h2>來源</h2>" not in text or '<ul class="sources"><li>' not in text:
        err(name, "必須有「來源」章節，且至少一筆來源")
    if "【" in text or "】" in text:
        err(name, "還有模板的【佔位文字】沒有替換")
    tag = re.search(r'<span class="tag">([^<]*)</span>', text)
    tag = tag.group(1) if tag else None
    if tag not in SECTIONS:
        err(name, "tag 必須是「概念」或「模式」")
    if name not in all_index_links:
        err(name, "沒有在 index.html 出現連結")
    elif name not in EXEMPT_FROM_SECTIONS and tag in SECTIONS and name not in listed[tag]:
        err(name, f"tag 是「{tag}」，卡片必須放在 index.html 的 {SECTIONS[tag]}:START/END 區塊內")
    d = re.search(r'name="description" content="([^"]*)"', text)
    if d and not 30 <= len(d.group(1)) <= 100:
        err(name, f"description 長度須在 30～100 字（目前 {len(d.group(1))}）")
    for link in re.findall(r'href="([^"#]+\.html)"', text):
        if not (p.parent / link).resolve().exists():
            err(name, f"壞連結：{link}")

for link in all_index_links:
    if not (ROOT / "pages" / link).exists():
        err("index.html", f"連到不存在的頁面：pages/{link}")

if errors:
    print("❌ 檢查失敗：")
    print("\n".join("  - " + e for e in errors))
    sys.exit(1)
print(f"✅ 檢查通過（{len(pages)} 個頁面）")
