from rq import Connection, Queue, Worker
import time
if __name__ == '__main__':
    # Tell rq what Redis connection to use
    with Connection():
        Worker(q).work()
