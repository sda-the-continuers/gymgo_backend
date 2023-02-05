import os
from celery import Celery
from celery.schedules import crontab
from kombu import Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gymtime_backend.settings')
app = Celery('gymtime_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# CELERY SUBSCRIBES ITS WORKERS TO THESE QUEUES
# ADD YOUR QUEUES HERE
app.conf.task_queues = (
    Queue('high_priority', consumer_arguments={'x-priority': 10}),
    Queue('mid_priority', consumer_arguments={'x-priority': 5}),
    Queue('low_priority', consumer_arguments={'x-priority': 1}),
)

app.conf.beat_schedule = {
    'MAKE_RESERVES_DONE': {
        'task': 'reservation.tasks.make_reserves_done',
        'schedule': 30 * 60,  # every half an hour
    },
    'SEND_GYMTIME_MESSAGES': {
        'task': 'sms.tasks.send_messages.send_gymtime_messages',
        'schedule': crontab(minute='*/5')  # at every 5th minute
    },
}

