import psycopg2
from psycopg2.extras import RealDictCursor
from config import settings

def get_db_connection():
    conn = psycopg2.connect(
        host=settings.database_host,
        database=settings.database_name,
        user=settings.database_user,
        password=settings.database_password,
    )
    return conn

def get_items():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM items;')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items
