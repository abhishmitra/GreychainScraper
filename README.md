# WebCrawler
This is an asynchronous web scraper that can currently scrape between 50 and 100 urls a second. It uses a redis queue to push tasks to a background worker. A docker compose launches redis and postgres instances. Currently the API server and the rq worker have not completely been containerized but this can be completed in one to two days.



## Steps 
Install requirements
`cd app`

`pip install -r requirements.txt`

Launch web server

`python3 main.py`

Launch rq worker

`rq worker --url redis://0.0.0.0:6379`
