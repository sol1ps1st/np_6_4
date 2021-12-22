import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'np_6_4.settings')
app = Celery('np_6_4')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'news_for_week_every_monday_8am': {
        'task': 'news.tasks.mail_week_posts',
        # 'schedule': crontab(),
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
