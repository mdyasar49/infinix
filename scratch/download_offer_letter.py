import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('209.182.232.150', username='infogenx-api', password='infogenx-api@1234', timeout=10)
sftp = ssh.open_sftp()
sftp.get('/home/infogenx-api/htdocs/api.infogenx.com/routes/offer-letter.js', 'remote_offer_letter.js')
sftp.close()
ssh.close()
print("Downloaded remote_offer_letter.js successfully")
