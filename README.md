# WebCrawler
This is an asynchronous web scraper that can currently scrape between 50 and 100 urls a second. It uses a redis queue to push tasks to a background worker. A docker compose launches redis and postgres instances. Currently the API server and the rq worker have not completely been containerized but this can be completed in one to two days.



## Steps 

1. Launch redis and postgres

`docker compose build --up`

2. Use pgadmin4 or psql to create the database which will be used. In this case it's called 'scraper'

3. Install requirements

`cd app`

`pip install -r requirements.txt`

4. Launch web server

`python3 main.py`

5. Launch rq worker

`rq worker --url redis://0.0.0.0:6379`

6. Run tests
   
`python3 -m unittest discover`


## Todo
1. Complete containerization of api and worker code
2. Use an ORM for the database queries
