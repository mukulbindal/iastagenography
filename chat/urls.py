from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'tokenn$', views.tokenn, name="tokenn"),
    url(r'receivemsg$', views.receivemsg, name="receivemsg"),
    url(r'sendmsg$', views.sendmsg, name="sendmsg"),
    url(r'readmsg$', views.readmsg, name="readmsg"),
    url(r'checkspam$', views.checkspam, name="checkspam"),
    url(r'rooms/(?P<slug>[-\w]+)/$', views.room_detail, name="room_detail"),
]


