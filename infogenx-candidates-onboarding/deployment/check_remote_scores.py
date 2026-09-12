import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('209.182.232.150', username='infogenx-candidates', password=os.environ.get('SSH_CAND_PASSWORD', 'infogenx@1234'), timeout=10)
stdin, stdout, stderr = ssh.exec_command('grep -rn "/ 50" /home/infogenx-candidates/htdocs/candidates.infogenx.com/src')
print(stdout.read().decode('utf-8'))
stdin, stdout, stderr = ssh.exec_command('grep -rn "/50" /home/infogenx-candidates/htdocs/candidates.infogenx.com/src')
print(stdout.read().decode('utf-8'))
ssh.close()
