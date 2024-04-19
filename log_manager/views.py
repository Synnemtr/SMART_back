from django.shortcuts import render
from rest_framework.permissions import IsAdminUser
from log_manager.models import Log
from log_manager.serializers import LogSerializer
from rest_framework.decorators import permission_classes, api_view


@api_view(['GET'])
@permission_classes([IsAdminUser])
def table_log(request):
    user = request.query_params.get('user', None)
    data_log = Log.objects.get_logs(user)
    last_updated = Log.objects.get_last_updated()
    serializer = LogSerializer(data_log, many=True)
    context = {'d': serializer.data, 'last_updated': last_updated}
    return render(request, 'log_manager/table_log.html', context)
