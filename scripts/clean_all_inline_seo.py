import os
import re

base = r"d:\infonix\infogenx.com.au\src\pages"

def clean_page(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 1. Remove import SEO from ...
    content = re.sub(r'import\s+SEO\s+from\s+[\'"][^\'"]+[\'"];?\r?\n?', '', content)

    # 2. Remove <SEO ... /> self-closing tag or <SEO>...</SEO>
    content = re.sub(r'<SEO\b[^>]*\/>\r?\n?', '', content)
    content = re.sub(r'<SEO\b[^>]*>[\s\S]*?<\/SEO>\r?\n?', '', content)

    if content != original:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

modified_count = 0
for root, dirs, files in os.walk(base):
    for file in files:
        if file.endswith(".jsx") or file.endswith(".js"):
            full_p = os.path.join(root, file)
            # Skip product child screens as requested
            if any(x in full_p for x in ["IGXStock", "OdooErp", "RetailPos", "CustomerRelation"]):
                continue
            if clean_page(full_p):
                print(f"Cleaned SEO in: {os.path.relpath(full_p, base)}")
                modified_count += 1

print(f"\nTotal files cleaned: {modified_count}")
