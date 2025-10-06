#!/usr/bin/env python
from decouple import config
import dj_database_url
import psycopg2

DATABASE_URL = config('DATABASE_URL')
cfg = dj_database_url.parse(DATABASE_URL)
conn = psycopg2.connect(dbname=cfg['NAME'], user=cfg['USER'], password=cfg['PASSWORD'], host=cfg['HOST'] or 'localhost', port=cfg['PORT'] or 5432)
with conn.cursor() as cur:
    cur.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;")
    for row in cur.fetchall():
        print(row)
conn.close()
