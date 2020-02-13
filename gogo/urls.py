from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'gogo/', views.get_anime_list, name="anime_list"),
    url(r'psit/', views.save_photos, name="psit"),
    url(r'listofurl/', views.listofurl, name="list_of_url")
]


