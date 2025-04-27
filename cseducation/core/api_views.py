from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import EventLog
from .serializers import EventLogSerializer
from .pagination import EventLogPagination

@api_view(['GET'])
@permission_classes([IsAdminUser])
def eventlog_list(request):
    """API endpoint for listing recent EventLog entries for analytics dashboard with pagination."""
    logs = EventLog.objects.order_by('-timestamp')
    paginator = EventLogPagination()
    page = paginator.paginate_queryset(logs, request)
    serializer = EventLogSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)
