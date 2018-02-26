from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^profile', views.personal_profile, name="my_submit"),
]