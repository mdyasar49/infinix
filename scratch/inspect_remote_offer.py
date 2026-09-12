import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('209.182.232.150', username='infogenx-api', password='infogenx-api@1234', timeout=10)
stdin, stdout, stderr = ssh.exec_command('grep -n -C 5 "request-approval" /home/infogenx-api/htdocs/api.infogenx.com/routes/offer-letter.js')
print(stdout.read().decode('utf-8'))

stdin, stdout, stderr = ssh.exec_command('grep -n -C 5 "Dear " /home/infogenx-api/htdocs/api.infogenx.com/routes/offer-letter.js')
print("--- DEAR MATCHES ---")
print(stdout.read().decode('utf-8'))
ssh.close()
