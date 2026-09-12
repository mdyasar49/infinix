import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

print("Connecting to infogenx-api...")
ssh_api = paramiko.SSHClient()
ssh_api.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_api.connect('209.182.232.150', username='infogenx-api', password=os.environ.get('SSH_API_PASSWORD', 'infogenx-api@1234'), timeout=15)

sftp_api = ssh_api.open_sftp()
print("Uploading remote_candidate_auth.js -> /home/infogenx-api/htdocs/api.infogenx.com/routes/candidate-auth.js")
sftp_api.put('remote_candidate_auth.js', '/home/infogenx-api/htdocs/api.infogenx.com/routes/candidate-auth.js')

print("Uploading remote_offer_letter.js -> /home/infogenx-api/htdocs/api.infogenx.com/routes/offer-letter.js")
sftp_api.put('remote_offer_letter.js', '/home/infogenx-api/htdocs/api.infogenx.com/routes/offer-letter.js')
sftp_api.close()

stdin, stdout, stderr = ssh_api.exec_command('pm2 restart all || pm2 restart api.infogenx.com')
print("PM2 restart output:", stdout.read().decode('utf-8'))
ssh_api.close()
print("infogenx-api update complete!")

print("Connecting to infogenx-candidates...")
ssh_cand = paramiko.SSHClient()
ssh_cand.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_cand.connect('209.182.232.150', username='infogenx-candidates', password=os.environ.get('SSH_CAND_PASSWORD', 'infogenx@1234'), timeout=15)

sftp_cand = ssh_cand.open_sftp()
print("Uploading candidates_ResultPage.jsx -> /home/infogenx-candidates/htdocs/candidates.infogenx.com/src/pages/ResultPage.jsx")
sftp_cand.put('candidates_ResultPage.jsx', '/home/infogenx-candidates/htdocs/candidates.infogenx.com/src/pages/ResultPage.jsx')
sftp_cand.close()

build_cmd = """
export PATH="/home/infogenx-candidates/.nvm/versions/node/v20.20.2/bin:$PATH"
cd /home/infogenx-candidates/htdocs/candidates.infogenx.com
node -v
npm run build
"""
stdin, stdout, stderr = ssh_cand.exec_command(build_cmd)
out = stdout.read().decode('utf-8')
err = stderr.read().decode('utf-8')
print("Build output:")
print(out)
if err:
    print("Build stderr:", err)

ssh_cand.close()
print("infogenx-candidates frontend rebuild complete!")
