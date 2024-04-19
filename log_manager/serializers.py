from rest_framework import serializers
from log_manager.models import Log


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id', 'date', 'time', 'user',
                  'method', 'path', 'response_time',
                  'message', 'status_code']
