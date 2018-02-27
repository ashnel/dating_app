from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^dashboard', views.dashboard, name="my_submit"),
    url(r'logout$', views.logout, name='my_logout'),
    url(r'settings$', views.settings, name='my_settings'),
    url(r'^update$', views.update, name="my_update"),
]