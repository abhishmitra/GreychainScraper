# docker run -h 0.0.0.0 --name redis-server -d redis
# rq worker --url redis://0.0.0.0:6379


from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from rq import Queue
from redis import Redis
import re

from database import verify_database_connection, create_tables_if_not_exist, list_all_tables, view_all_rows, insert_row
from worker import background_task

app = Flask(__name__)


@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing."}), 400

    job = queue.enqueue(background_task, url)
    return jsonify({"job_id": job.get_id()}), 202

@app.route('/search', methods=['GET'])
def search():
    search_text = request.args.get('search_text')
    if not search_text:
        return jsonify({"error": "Search text parameter is missing."}), 400

    #search_engine = SearchEngine(data)
    #results = search_engine.search_text(search_text)
    return jsonify("Hello") #jsonify({"results": results}), 200

if __name__ == '__main__':

    #####
    print(verify_database_connection())
    print(list_all_tables())
    print(insert_row("abc", "def"))
    print(view_all_rows())
    #####

    if verify_database_connection():
        create_tables_if_not_exist()
        app.run(debug=True)
    else:
        print("Exiting due to database connection failure.")