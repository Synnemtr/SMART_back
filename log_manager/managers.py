from django.db import models
from django.db import connection


class LogManager(models.Manager):
    def get_logs(self, user=None):
        if user is not None:
            return self.filter(user=user)
        return self.all()

    def get_last_updated(self):
        query = """
                SELECT MAX(updated_at) FROM log_user
                """
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            return row[0]
