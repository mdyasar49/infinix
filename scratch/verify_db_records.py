import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('209.182.232.150', username='infogenx-api', password='infogenx-api@1234', timeout=10)

check_cmd = """cd /home/infogenx-api/htdocs/api.infogenx.com && node -e "
const mysql = require('mysql2/promise');
require('dotenv').config({ path: '/home/infogenx-api/htdocs/api.infogenx.com/.env' });
(async () => {
  const pool = mysql.createPool({
    host: process.env.DB_HOST || '127.0.0.1',
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
  });
  const [rows] = await pool.query('SELECT id, candidate_name, candidate_email, assessment_score, status, owner_notified_at, candidate_notified_at FROM candidate_offer_requests ORDER BY id DESC LIMIT 5');
  console.log(JSON.stringify(rows, null, 2));
  process.exit();
})();
"
"""

stdin, stdout, stderr = ssh.exec_command(check_cmd)
print(stdout.read().decode('utf-8'))
err = stderr.read().decode('utf-8')
if err:
    print("Stderr:", err)
ssh.close()
