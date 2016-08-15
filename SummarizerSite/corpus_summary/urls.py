from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.summarize, name='summarize'),
    url(r'^create_post/$', views.summarize_POST)
]