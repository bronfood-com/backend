from dramatiq_crontab import cron
import dramatiq
from django.contrib.auth import get_user_model

User = get_user_model()


@cron('* * * * *')
@dramatiq.actor
def my_task():
    print(User.objects.all())
