import subprocess

plink = r'C:\Program Files\PuTTY\plink.exe'
cmd = [plink, '-ssh', '-batch', '-pw', 'infogenx@1234', 'infogenx-onboarding@209.182.232.150', 'curl -i http://127.0.0.1 -H "Host: onboarding.infogenx.com"']

p = subprocess.run(cmd, capture_output=True, text=True, input='y\n')
print(p.stdout[:1000])
