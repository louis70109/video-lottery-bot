import psycopg2
import psycopg2.extras

import urllib.parse as urlparse
import os

URL = urlparse.urlparse(os.getenv('DATABASE_URL'))
DB_NAME = URL.path[1:]
USER = URL.username
PASSWORD = URL.password
HOST = URL.hostname
PORT = URL.port


class Database:
    conns = []

    def __enter__(self):
        return self

    def connect(self):
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        self.conns.append(conn)

        return conn

    def __exit__(self, type, value, traceback):
        for conn in self.conns:
            conn.close()

        self.conns.clear()


def create_lottery(line_id: str, name: str):
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f'''
            INSERT INTO lottery(line_id, name) 
            VALUES ('{line_id}', '{name}')
            ON CONFLICT 
            ON CONSTRAINT event_line_unique 
            DO NOTHING
            RETURNING *
        ''')
        conn.commit()
        row = cur.fetchone()
    return row


def count_lottery():
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute('select count(*) from lottery')
        count = cur.fetchone()['count']
    return count
