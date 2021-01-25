from subscribers_service.config.celery import celery
from flask import  render_template

from .cache import ReadCache

from .publisher import Publish


@celery.task(name='send_mail_to_subscribers', task_time_limit=60, task_soft_time_limit=50,
             acks_late=True, autoretry_for=(Exception,), retry_backoff=True,
             retry_jitter=False, retry_kwargs={'max_retries': 3}, retry_backoff_max=60)
def send_mail_to_subscribers():
    cache = ReadCache()
    post_list = cache.load_data()
    print('post_list', post_list)
    to = ['idris.sabanli@gmail.com', 'idris.sabanli@tech.edu.az']
    if not post_list or not to:
        return False
    body = render_template('subscribers_email.html', post_list=post_list)

    subject = 'New posts from Stories'
    subtype = 'html'
    data = {
        'subject': subject,
        'body': body,
        'to': to,
        'subtype': subtype,
    }
    event_type = 'send_mail'
    Publish(data=data, event_type=event_type)
    cache.delete()
    return True
