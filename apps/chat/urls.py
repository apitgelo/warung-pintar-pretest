from django.conf.urls import url, include

from .views import message

urlpatterns = [
    url(r'^chats/', include([
        url(r'^$', message.MessageViewSet.as_view({"get": "list", "post": "create"}), name="meeting-list"),
    ]))
]