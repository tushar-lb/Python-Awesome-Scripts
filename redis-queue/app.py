import os
import time
from rq import Connection, Queue
from messanger import display
import sys

def main():
    message = sys.argv[1]
    async_results = {}
    q = Queue()
    async_results[message] = q.enqueue(display,message)
    start_time = time.time()
    done = False
    while not done:
        os.system('clear')
        print('Asynchronously: (now = %.2f)' % (time.time() - start_time,))
        done = True
	result = async_results[message].return_value
	if result is None:
	    done = False
	    result = 'in progress...'
        print('Hello %s, Welcome,Nice to meet you ..:)'%(result))
        print('')
        print('To start the processing in the background, run a worker:')
        time.sleep(0.2)
    print('Done')


if __name__ == '__main__':
    # Tell RQ what Redis connection to use
    with Connection():
        main()
