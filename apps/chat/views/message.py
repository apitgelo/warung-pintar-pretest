from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from ..models.message import Message

from ..serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.order_by("-id")
    serializer_class = MessageSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        paginator = LimitOffsetPagination()
        queryset = paginator.paginate_queryset(self.queryset, request)
        serializer = MessageSerializer(queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
