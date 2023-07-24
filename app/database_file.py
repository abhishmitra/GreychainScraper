import psycopg2
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from rq import Queue
from redis import Redis
import re

# PostgreSQL database configuration
db_params = {
    'dbname': 'greychain',
    'user': 'postgres',
    'password': 'postgres',
    'host': '0.0.0.0',
    'port': '5432'
}
queue = Queue(connection=Redis(host="0.0.0.0", port=6379))
#queue = Queue(connection=Redis(host="0.0.0.0", port=6379))


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