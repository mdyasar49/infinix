import os
import re
import sys

base = r'd:\infonix'

projects = {
    'AU Site (.com.au)': r'd:\infonix\infogenx.com.au',
    'COM Site (.com)': r'd:\infonix\infogenx.com',
    'DEV Site (dev)': r'd:\infonix\dev'
}

def run_guard():
    print("=" * 60)
    print("INFOGENX AUTOMATED SEO & PERFORMANCE REGRESSION GUARD")
    print("=" * 60)

    total_checks = 0
    failed_checks = 0

    for name, path in projects.items():
        print(f"\nAuditing {name} [{path}]...")

        # 1. Check Typo Redirect in paths.js & index.js
        paths_file = os.path.join(path, 'src', 'route', 'paths.js')
        index_file = os.path.join(path, 'src', 'route', 'index.js')
        
        total_checks += 2
        if os.path.exists(paths_file) and '/mobile-app-developement' in open(paths_file, encoding='utf-8').read():
            print("  [PASS] Typo URL path registered in paths.js")
        else:
            print("  [FAIL] Missing typo URL path in paths.js")
            failed_checks += 1

        if os.path.exists(index_file) and 'mobileAppTypoLegacy' in open(index_file, encoding='utf-8').read():
            print("  [PASS] Typo URL 301 redirect registered in index.js")
        else:
            print("  [FAIL] Missing typo 301 redirect in index.js")
            failed_checks += 1

        # 2. Check Passive Scroll Listeners
        total_checks += 2
        exp_file = os.path.join(path, 'src', 'sections', 'Home', 'Expertise', 'Expertise.jsx')
        sh_file = os.path.join(path, 'src', 'sections', 'Home', 'ServiceHighlight', 'ServiceHighlight.jsx')
        
        if os.path.exists(exp_file) and 'passive: true' in open(exp_file, encoding='utf-8').read():
            print("  [PASS] Expertise.jsx uses passive scroll listener")
        else:
            print("  [FAIL] Expertise.jsx missing passive scroll listener")
            failed_checks += 1

        if os.path.exists(sh_file) and 'passive: true' in open(sh_file, encoding='utf-8').read():
            print("  [PASS] ServiceHighlight.jsx uses passive scroll listener")
        else:
            print("  [FAIL] ServiceHighlight.jsx missing passive scroll listener")
            failed_checks += 1

        # 3. Check Canonical Fallback in SEO.jsx
        seo_file = os.path.join(path, 'src', 'components', 'SEO', 'SEO.jsx')
        total_checks += 1
        if os.path.exists(seo_file) and 'currentCanonical' in open(seo_file, encoding='utf-8').read():
            print("  [PASS] SEO.jsx includes automatic canonical fallback")
        else:
            print("  [FAIL] SEO.jsx missing automatic canonical fallback")
            failed_checks += 1

        # 4. Check Hero Video Deferral in NetworkBackground.jsx
        bg_file = os.path.join(path, 'src', 'components', 'NetworkBackground', 'NetworkBackground.jsx')
        total_checks += 1
        if os.path.exists(bg_file) and 'shouldLoadVideo' in open(bg_file, encoding='utf-8').read() and 'preload="none"' in open(bg_file, encoding='utf-8').read():
            print("  [PASS] NetworkBackground.jsx has video payload deferral")
        else:
            print("  [FAIL] NetworkBackground.jsx missing video payload deferral")
            failed_checks += 1

        # 5. Check index.html cleanliness
        idx_file = os.path.join(path, 'public', 'index.html')
        total_checks += 1
        if os.path.exists(idx_file) and 'gtm-noscript' in open(idx_file, encoding='utf-8').read():
            print("  [PASS] index.html has clean GTM class (no inline style warning)")
        else:
            print("  [FAIL] index.html missing clean GTM class")
            failed_checks += 1

    print("\n" + "=" * 60)
    print(f"SUMMARY: Total Checks: {total_checks} | Passed: {total_checks - failed_checks} | Failed: {failed_checks}")
    print("=" * 60)
    
    if failed_checks == 0:
        print("\nPERFECT! ZERO ISSUES FOUND ACROSS ALL 3 ECOSYSTEM ENVIRONMENTS!")
        return 0
    else:
        print(f"\nWARNING: {failed_checks} regression issues detected.")
        return 1

if __name__ == '__main__':
    sys.exit(run_guard())
