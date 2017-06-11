class RedisTools:
    '''
    A set of utility tools for interacting with a redis cache
    '''

    def __init__(self):
        self._queues = ["default", "high", "low", "failed"]
        self.get_redis_connection()

    def get_redis_connection(self):
        redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
        self.redis = redis.from_url(redis_url)

    def get_queues(self):
        return self._queues

    def get_queue_count(self, queue):
        return Queue(name=queue, connection=self.redis).count

    def msg_print_log(self, msg):
        print msg
        logger.info(msg)

    def get_key_count(self):
        return len(self.redis.keys('rq:job:*'))

    def get_queue_job_counts(self):
        queues = self.get_queues()
        queue_counts = [self.get_queue_count(queue) for queue in queues]
        return zip(queues, queue_counts)

    def has_orphanes(self):
        job_count = sum([count[1] for count in self.get_queue_job_counts()])
        return job_count < self.get_key_count()

    def print_failed_jobs(self):
        q = django_rq.get_failed_queue()
        while True:
            job = q.dequeue()
            if not job:
                break
            print job

    def print_job_counts(self):
        for queue in self.get_queue_job_counts():
            print "{:.<20}{}".format(queue[0], queue[1])
        print "{:.<20}{}".format('Redis Keys:', self.get_key_count())

    def delete_failed_jobs(self):
        q = django_rq.get_failed_queue()
        count = 0
        while True:
            job = q.dequeue()
            if not job:
                self.msg_print_log("{} Jobs deleted.".format(count))
                break
            job.delete()
            count += 1

    def delete_orphaned_jobs(self):
        if not self.has_orphanes():
            return self.msg_print_log("No orphan jobs to delete.")

        for i, key in enumerate(self.redis.keys('rq:job:*')):
            job_number = key.split("rq:job:")[1]
            job = Job.fetch(job_number, connection=self.redis)
            job.delete()
            self.msg_print_log("[{}] Deleted job {}.".format(i, job_number))
