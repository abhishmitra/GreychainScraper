# WebCrawler
This is an asynchronous web scraper that can currently scrape between 50 and 100 urls a second. It consists of 4 services:
api - A webserver that accepts scraping and searching requests
worker - An rq worker that processes web scraping requests sent to a redis queue
redis - Used for storing the list of sites to scrape
postgres - Used to store the scraped results




## Steps 

1. Launch the services

`docker compose build --up`

2. Run tests
   
`python3 -m unittest discover`


## Todo
1. Use an ORM for the database queries
