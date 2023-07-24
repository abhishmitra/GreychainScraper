import psycopg2
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re

# PostgreSQL database configuration
db_params = {
    'dbname': 'greychain',
    'user': 'postgres',
    'password': 'postgres',
    'host': '0.0.0.0',
    'port': '5432'
}


def search_text_in_data(search_text):
    try:
        db_conn = psycopg2.connect(**db_params)
        db_cursor = db_conn.cursor()

        # Using parameterized query to prevent SQL injection
        search_query = "SELECT url, content FROM scraped_data WHERE content ILIKE %s"
        data = ('%' + search_text + '%',)
        db_cursor.execute(search_query, data)
        rows = db_cursor.fetchall()

        db_conn.close()
        return rows
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return []



def list_all_tables():
    try:
        db_conn = psycopg2.connect(**db_params)
        db_cursor = db_conn.cursor()

        db_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        table_names = [row[0] for row in db_cursor.fetchall()]

        db_conn.close()
        return table_names
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return []

def create_tables_if_not_exist():
    try:
        db_conn = psycopg2.connect(**db_params)
        db_cursor = db_conn.cursor()

        db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS scraped_data (
                url VARCHAR PRIMARY KEY,
                content TEXT
            )
        """)
        db_conn.commit()
        db_conn.close()
    except psycopg2.Error as e:
        print("Error creating tables:", e)

def verify_database_connection():
    try:
        db_conn = psycopg2.connect(**db_params)
        db_conn.close()
        return True
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return False


def view_all_rows():

    try:
        db_conn = psycopg2.connect(**db_params)
        db_cursor = db_conn.cursor()

        db_cursor.execute("SELECT * FROM scraped_data")
        rows = db_cursor.fetchall()

        db_conn.close()
        return rows
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return []


def insert_row(url, content):
    try:
        db_conn = psycopg2.connect(**db_params)
        db_cursor = db_conn.cursor()

        # Using parameterized query to prevent SQL injection
        insert_query = "INSERT INTO scraped_data (url, content) VALUES (%s, %s)"
        data = (url, content)
        db_cursor.execute(insert_query, data)

        db_conn.commit()
        db_conn.close()
        return True
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return False


def get_unique_urls():
    unique_urls = []
    try:
        db_conn = psycopg2.connect(**db_params)
        db_cursor = db_conn.cursor()

        select_query = "SELECT DISTINCT url FROM scraped_data"
        db_cursor.execute(select_query)

        unique_urls = [row[0] for row in db_cursor.fetchall()]

        db_conn.close()
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

    return set(unique_urls)



def delete_all_rows():
    try:
        with psycopg2.connect(**db_params) as db_conn:
            with db_conn.cursor() as db_cursor:
                delete_query = "DELETE FROM scraped_data"
                db_cursor.execute(delete_query)
                db_conn.commit()
        print("All rows deleted successfully.")
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

def fetch_non_empty_text_rows():
    empty_text_rows = []
    try:
        db_conn = psycopg2.connect(**db_params)
        db_cursor = db_conn.cursor()

        select_query = "SELECT url FROM scraped_data WHERE content IS NOT NULL AND url != ''"
        db_cursor.execute(select_query)
        rows = db_cursor.fetchall()

        empty_text_rows = [row[0] for row in rows]

        db_conn.close()
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

    return empty_text_rows


def count_empty_rows():
    try:
        db_conn = psycopg2.connect(**db_params)
        db_cursor = db_conn.cursor()

        count_query = "SELECT COUNT(*) FROM scraped_data WHERE content IS NULL"
        db_cursor.execute(count_query)
        count = db_cursor.fetchone()[0]

        db_conn.close()

        return count

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return -1


def fetch_empty_text_rows(limit=100):
    empty_text_rows = []
    try:
        db_conn = psycopg2.connect(**db_params)
        db_cursor = db_conn.cursor()

        select_query = "SELECT url FROM scraped_data WHERE content IS NULL AND url != '' LIMIT %s"
        db_cursor.execute(select_query, (limit,))
        rows = db_cursor.fetchall()

        empty_text_rows = [row[0] for row in rows]

        db_conn.close()
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

    return empty_text_rows

def update_database_with_content(url, content):
    try:
            db_conn = psycopg2.connect(**db_params)
            db_cursor = db_conn.cursor()

            update_query = "UPDATE scraped_data SET content = %s WHERE url = %s"

            db_cursor.execute(update_query, (content, url))
            db_conn.commit()
            db_conn.close()
    except psycopg2.Error as e:
        print("Error updating database:", e)


def insert_urls_with_content(urls):
    try:
        db_conn = psycopg2.connect(**db_params)
        db_cursor = db_conn.cursor()

        insert_query = "INSERT INTO scraped_data (url, content) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        db_cursor.executemany(insert_query, urls)

        db_conn.commit()
        db_conn.close()

    except psycopg2.Error as e:
        print("Error connecting to the database:", e)