#!/usr/bin/env python
"""
Simple exporter that queries selected tables and writes INSERT statements to a .sql file.
NOT for large datasets; intended for small mock export.
"""
import os
import sys
import urllib.parse
from decouple import config
import dj_database_url
import psycopg2
from psycopg2 import sql

BASE_DIR = os.path.dirname(__file__)
DATABASE_URL = config('DATABASE_URL', default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'))

cfg = dj_database_url.parse(DATABASE_URL)

if cfg['ENGINE'] != 'django.db.backends.postgresql':
    print('Warning: Exporter expects a PostgreSQL DB; exporting may not work as intended for sqlite or others.')

conn_params = {
    'dbname': cfg.get('NAME'),
    'user': cfg.get('USER'),
    'password': cfg.get('PASSWORD'),
    'host': cfg.get('HOST') or 'localhost',
    'port': cfg.get('PORT') or 5432,
}

outfile = os.path.join(BASE_DIR, 'mock_data.sql')

def fetch_table(cursor, table):
    cursor.execute(sql.SQL('SELECT * FROM {}').format(sql.Identifier(table)))
    cols = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    return cols, rows


def format_value(v):
    if v is None:
        return 'NULL'
    if isinstance(v, str):
        return "'" + v.replace("'", "''") + "'"
    if isinstance(v, bytes):
        return "E'\\x" + v.hex() + "'"
    return str(v)


def export_tables(tables):
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            with open(outfile, 'w', encoding='utf-8') as f:
                f.write('-- Mock data export\n')
                f.write('BEGIN;\n')
                for t in tables:
                    print('Exporting', t)
                    cols, rows = fetch_table(cur, t)
                    if not rows:
                        continue
                    for r in rows:
                        vals = ', '.join(format_value(x) for x in r)
                        query = f"INSERT INTO {t} ({', '.join(cols)}) VALUES ({vals});\n"
                        f.write(query)
                f.write('COMMIT;\n')

if __name__ == '__main__':
    tables = [
        'career_career',
        'user_user',
        'achievement_achievement',
        'achievement_userachievement',
    ]
    export_tables(tables)
    print('Export complete ->', outfile)
