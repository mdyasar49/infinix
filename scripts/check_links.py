import re
import os

base = r"d:\infonix\infogenx.com.au"

# 1. Parse paths.js
with open(os.path.join(base, "src", "route", "paths.js"), "r", encoding="utf-8") as f:
    paths_raw = f.read()

paths_dict = {}
for line in paths_raw.splitlines():
    m = re.search(r"(\w+):\s*[\"']([^\"']+)[\"']", line)
    if m:
        paths_dict[m.group(1)] = m.group(2)

# 2. Parse elements.js
with open(os.path.join(base, "src", "route", "elements.js"), "r", encoding="utf-8") as f:
    elem_raw = f.read()

elem_map = {}
for line in elem_raw.splitlines():
    m = re.search(r"export const (\w+)\s*=\s*(?:Loadable\(lazy\(\(\)\s*=>\s*import\([\"']([^\"']+)[\"']\)\)|.*?import\([\"']([^\"']+)[\"']\)|.*?<(\w+Component))", line)
    if m:
        name = m.group(1)
        rel_path = m.group(2) or m.group(3) or m.group(4)
        elem_map[name] = rel_path

# 3. Parse index.js (Router)
with open(os.path.join(base, "src", "route", "index.js"), "r", encoding="utf-8") as f:
    router_raw = f.read()

routes = []
for line in router_raw.splitlines():
    m = re.search(r"\{\s*path:\s*(?:PATHS\.(\w+)|[\"']([^\"']+)[\"']),\s*element:\s*(<.*?>)\s*\}", line)
    if m:
        p_key = m.group(1)
        p_val = m.group(2)
        target_path = paths_dict.get(p_key, p_val)
        elem_str = m.group(3)
        routes.append((target_path, elem_str))

print("=== ALL REGISTERED ROUTES IN ROUTER ===")
for r in routes:
    print(f"{r[0]} -> {r[1]}")

# 4. Check Products Page vs Isolated Products
print("\n=== ISOLATED ROUTES (MainLayout.jsx) ===")
with open(os.path.join(base, "src", "layouts", "MainLayout.jsx"), "r", encoding="utf-8") as f:
    ml_raw = f.read()
print(re.findall(r"[\"'](/products/[^\"']+|/blog/admin/[^\"']+)[\"']", ml_raw))

# 5. Check Header Nav items
with open(os.path.join(base, "src", "sections", "Header", "Header.jsx"), "r", encoding="utf-8") as f:
    h_raw = f.read()
print("\n=== HEADER DIRECT LINKS ===")
print(re.findall(r"\{\s*name:\s*[\"']([^\"']+)[\"'],\s*path:\s*[\"']([^\"']+)[\"']", h_raw))

# 6. Check Products page content
products_page_file = os.path.join(base, "src", "pages", "Products", "Products.jsx")
if os.path.exists(products_page_file):
    with open(products_page_file, "r", encoding="utf-8") as f:
        print("\n=== Products.jsx Preview ===")
        print(f.read()[:500])
