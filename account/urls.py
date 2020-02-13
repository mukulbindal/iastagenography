from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name="dashboard"),
    url(r'isusernameavailable$',views.isUsernameAvaliable , name = "isUsernameAvaliable"),
    url(r'getchatkey$',views.getchatkey , name = "getchatkey"),
    
]


