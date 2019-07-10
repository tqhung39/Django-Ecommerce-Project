from django.conf.urls import url
from django.contrib import admin
from search import views

app_name = 'search'
urlpatterns = [
    url(r'^$', views.searchbook, name='searchbooks'),
]