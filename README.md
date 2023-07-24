# WebCrawler
This is an asynchronous web scraper that can currently scrape between 50 and 100 urls a second. It consists of 4 services:
api - A webserver that accepts scraping and searching requests
worker - An rq worker that processes web scraping requests sent to a redis queue
redis - Used for storing the list of sites to scrape
postgres - Used to store the scraped results


![Screenshot 2023-07-24 160819](https://github.com/abhishmitra/WebCrawler/assets/4780519/d22d2e1f-7729-4a67-aa53-b2c6c548f69e)


![Screenshot 2023-07-24 161209](https://github.com/abhishmitra/WebCrawler/assets/4780519/0f8661ad-fae0-40b1-a58d-e174364241b0)



## Steps 

1. Launch the services

`docker compose build --up`

2. Run tests
   
`python3 -m unittest discover`


## Todo
1. Use an ORM for the database queries
