import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('209.182.232.150', username='infogenx-candidates', password='infogenx@1234', timeout=10)
stdin, stdout, stderr = ssh.exec_command('cat /home/infogenx-candidates/htdocs/candidates.infogenx.com/src/pages/ResultPage.jsx')
content = stdout.read().decode('utf-8')
with open('candidates_ResultPage.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved candidates_ResultPage.jsx, length:', len(content))
ssh.close()
