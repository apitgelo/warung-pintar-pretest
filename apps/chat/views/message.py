import pusher
from rest_framework import viewsets, serializers, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)

        if serializer.is_valid():
            message = Message.objects.create(text=serializer.validated_data["text"])

            channels_client = pusher.Pusher(
                app_id='866721',
                key='374c69e5a5679fd521b4',
                secret='a4860685791e6ef41792',
                cluster='ap1',
                ssl=True
            )

            channels_client.trigger('my-channel', 'my-event', {'message': message.text})

            return Response({'detail': 'Success', 'text': message.text}, status=status.HTTP_200_OK)
        else:
            raise serializers.ValidationError(serializer.errors)

