from app.models import BaseEntity
from django.db import models
from log_manager.managers import LogManager


class Log(BaseEntity):
    class Meta:
        db_table = 'log_user'
        ordering = ['-id']
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    user = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    response_time = models.FloatField(default=0)
    message = models.CharField(max_length=255)
    status_code = models.IntegerField(default=0)
    objects = LogManager()
