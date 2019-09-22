from django.conf.urls import url, include

from .views import message

urlpatterns = [
    url(r'^chat/', include([
        url(r'^$', message.MessageViewSet.as_view({"get": "list"}), name="meeting-list"),
    ]))
]