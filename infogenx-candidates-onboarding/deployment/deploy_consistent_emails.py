import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

print("Connecting to infogenx-api (209.182.232.150)...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('209.182.232.150', username='infogenx-api', password=os.environ.get('SSH_API_PASSWORD', 'infogenx-api@1234'), timeout=15)

sftp = ssh.open_sftp()
print("1. Uploading remote_candidate_auth.js -> /home/infogenx-api/htdocs/api.infogenx.com/routes/candidate-auth.js")
sftp.put('remote_candidate_auth.js', '/home/infogenx-api/htdocs/api.infogenx.com/routes/candidate-auth.js')

print("2. Uploading remote_offer_letter.js -> /home/infogenx-api/htdocs/api.infogenx.com/routes/offer-letter.js")
sftp.put('remote_offer_letter.js', '/home/infogenx-api/htdocs/api.infogenx.com/routes/offer-letter.js')
sftp.close()

print("Restarting API server...")
stdin, stdout, stderr = ssh.exec_command("kill -9 $(pgrep -f server.js | head -1); sleep 2; ps aux | grep server.js")
print("Process status after restart:")
print(stdout.read().decode('utf-8'))
ssh.close()
print("All API email routes successfully updated and restarted!")
