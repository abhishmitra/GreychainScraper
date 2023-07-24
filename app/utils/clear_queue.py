from rq import Queue
from redis import Redis

queue = Queue(connection=Redis(host="0.0.0.0", port=6379))
queue.empty()

print(len(queue.jobs))