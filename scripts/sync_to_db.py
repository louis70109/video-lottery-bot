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


print("Check database status...")
try:
    with Database() as db, db.connect() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(f'''
            CREATE TABLE public.lottery
            (
                line_id character varying(100) COLLATE pg_catalog."default",
                name character varying(100) COLLATE pg_catalog."default",
                CONSTRAINT event_line_unique UNIQUE (line_id, name)
                    INCLUDE(line_id, name)
            )
            
            TABLESPACE pg_default;

            ALTER TABLE public.lottery
                OWNER to {USER};
        ''')
        conn.commit()
except psycopg2.errors.DuplicateTable:
    print('Tables have been create.')
    pass
except Exception as e:
    raise Exception(e)
print("Sync database complete!")
