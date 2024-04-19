from apscheduler.schedulers.background import BackgroundScheduler
from app import settings
import os
from log_manager.models import Log
import pandas as pd


def update_database():
    num_in_db = Log.objects.count()
    path = os.path.join(settings.BASE_DIR, 'logs/requests.csv')
    # Initialize data
    df = pd.read_csv(path)
    for i in range(num_in_db, len(df)):
        row = df.iloc[i]
        log = Log.objects.create(
            date=row['date'],
            time=row['time'],
            user=row['user'],
            method=row['method'],
            path=row['path'],
            response_time=row['response_time'],
            message=row['message'],
            status_code=row['status_code']
        )
        log.save()


def start():
    scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': '1'})
    scheduler.add_job(update_database, 'interval', seconds=20)
    scheduler.start()
