#!/usr/bin/env python
import os
import sys
import urllib.parse
import subprocess

env_path = os.path.join(os.path.dirname(__file__), '.env')
if not os.path.exists(env_path):
    print('.env file not found in project root')
    sys.exit(1)

with open(env_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

db_url = None
for line in lines:
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    if line.startswith('DATABASE_URL='):
        db_url = line.split('=', 1)[1].strip()
        break

if not db_url:
    print('DATABASE_URL not found in .env')
    sys.exit(1)

if db_url.startswith('postgres://') or db_url.startswith('postgresql://'):
    if db_url.startswith('postgres://'):
        prefix = 'postgres://'
        body = db_url[len(prefix):]
    else:
        prefix = 'postgresql://'
        body = db_url[len(prefix):]

    if '@' in body:
        creds, host = body.rsplit('@', 1)
        if ':' in creds:
            user, password = creds.split(':', 1)
            password_quoted = urllib.parse.quote(password, safe='')
            safe_db_url = prefix + user + ':' + password_quoted + '@' + host
        else:
            safe_db_url = db_url
    else:
        safe_db_url = db_url
else:
    safe_db_url = db_url

print('Using DB URL (masked):', safe_db_url.replace('/', '/').replace(':', ':'))

os.environ['DATABASE_URL'] = safe_db_url

ret = subprocess.run([sys.executable, 'manage.py', 'migrate', '--noinput'], cwd=os.path.dirname(__file__))
if ret.returncode != 0:
    print('migrate failed with exit code', ret.returncode)
    sys.exit(ret.returncode)

print('migrations completed successfully')
sys.exit(0)
