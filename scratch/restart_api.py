import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('209.182.232.150', username='infogenx-api', password='infogenx-api@1234', timeout=15)
sftp = ssh.open_sftp()
sftp.put('remote_offer_letter.js', '/home/infogenx-api/htdocs/api.infogenx.com/routes/offer-letter.js')
sftp.close()

stdin, stdout, stderr = ssh.exec_command("kill -9 $(pgrep -f server.js | head -1); sleep 2; ps aux | grep server.js")
print(stdout.read().decode('utf-8'))
ssh.close()
print("Restart completed.")
