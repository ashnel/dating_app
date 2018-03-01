from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^dashboard', views.dashboard, name="my_submit"),
    url(r'logout$', views.logout, name='my_logout'),
    url(r'settings$', views.settings, name='my_settings'),
    url(r'matches$', views.matches, name='my_matches'),
    url(r'new_match$', views.new_match),
    url(r'vote$', views.vote, name='my_vote'),
    url(r'^update$', views.update, name="my_update"),
]