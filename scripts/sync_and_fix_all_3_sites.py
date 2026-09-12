import os
import re

base = r'd:\infonix'

sites = ['dev', 'infogenx.com', 'infogenx.com.au']

def sync_and_fix():
    print("=" * 60)
    print("AUTOMATED SYNC & FIX ACROSS ALL 3 SITES (DEV, COM, AU)")
    print("=" * 60)

    # 1. Add preload="none" to all video tags across all 3 sites
    for s in sites:
        s_dir = os.path.join(base, s, 'src')
        video_fixes = 0
        for root, dirs, files in os.walk(s_dir):
            for file in files:
                if file.endswith('.jsx'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Pattern for video tags missing preload
                    if '<video' in content and 'preload=' not in content:
                        new_content = re.sub(r'<video(\s+)', r'<video preload="none"\1', content)
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        video_fixes += 1
        print(f"[{s}] Added preload=\"none\" to {video_fixes} video tags")

    # 2. Ensure About.jsx has SEO component in AU and COM
    for s in ['infogenx.com', 'infogenx.com.au']:
        about_path = os.path.join(base, s, 'src', 'pages', 'About', 'About.jsx')
        if os.path.exists(about_path):
            with open(about_path, 'r', encoding='utf-8') as f:
                c = f.read()
            if 'import SEO' not in c:
                c = 'import SEO from "../../components/SEO/SEO";\n' + c
                c = c.replace('<Breadcrumbs', '<SEO title="About Infogenx | AI Automation & IT Experts" description="Learn how Infogenx empowers businesses with AI applications, intelligent automation, and data analytics across Microsoft, Zoho, and Odoo ecosystems." />\n      <Breadcrumbs')
                with open(about_path, 'w', encoding='utf-8') as f:
                    f.write(c)
                print(f"[{s}] Added SEO component to About.jsx")

    print("\nSync and automated fixes completed successfully!")

if __name__ == '__main__':
    sync_and_fix()
