import os

base_dir = r"d:\infonix"
found_py = []

for root, dirs, files in os.walk(base_dir):
    if "node_modules" in root or ".git" in root or ".venv" in root:
        continue
    for f in files:
        if f.endswith(".py"):
            found_py.append(os.path.join(root, f))

print(f"Total Python files found: {len(found_py)}")
for p in sorted(found_py):
    print(p)
