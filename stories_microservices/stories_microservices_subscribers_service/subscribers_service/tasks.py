from subscribers_service.config.celery import celery

from subscribers_service.cache import ReadCache


@celery.task(name='send_mail_to_subscribers', task_time_limit=60, task_soft_time_limit=50,
             acks_late=True, autoretry_for=(Exception,), retry_backoff=True,
             retry_jitter=False, retry_kwargs={'max_retries': 3}, retry_backoff_max=60)
def send_mail_to_subscribers():
    cache = ReadCache()
    post_list = cache.load_data()
    print(post_list)
