import os
import re

base = r"d:\infonix\infogenx.com.au\src\pages"

# Check every page component in pages
all_pages = []
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".jsx") or f.endswith(".js"):
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, base)
            if any(x in rel_p for x in ["IGXStock", "OdooErp", "RetailPos", "CustomerRelation", "Admin"]):
                continue
            all_pages.append((rel_p, full_p))

print(f"Total non-product-child pages to inspect: {len(all_pages)}")

audit_results = []
for rel_p, full_p in all_pages:
    with open(full_p, "r", encoding="utf-8") as file:
        content = file.read()
    
    has_seo = bool(re.search(r"<SEO\b", content))
    has_breadcrumbs = bool(re.search(r"<Breadcrumbs\b", content))
    has_hero = bool(re.search(r"Hero|hero", content))
    has_faq = bool(re.search(r"Faq|faq", content))
    has_related = bool(re.search(r"RelatedServices|related", content, re.IGNORECASE))
    
    audit_results.append({
        "file": rel_p,
        "has_seo": has_seo,
        "has_breadcrumbs": has_breadcrumbs,
        "has_hero": has_hero,
        "has_faq": has_faq,
        "has_related": has_related,
    })

print("\n=== DETAILED SCREEN AUDIT ===")
for r in audit_results:
    seo_flag = "[!] INLINE SEO" if r["has_seo"] else "[OK] No SEO tag"
    bc_flag = "[OK] Breadcrumbs" if r["has_breadcrumbs"] else "[--] No BC"
    faq_flag = "[OK] FAQs" if r["has_faq"] else "[--] No FAQs"
    rel_flag = "[OK] Related Links" if r["has_related"] else "[--] No Related"
    print(f"{r['file']:<55} | {seo_flag:<16} | {bc_flag:<16} | {faq_flag:<12} | {rel_flag:<16}")
