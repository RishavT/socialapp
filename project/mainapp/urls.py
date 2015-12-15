from django.conf.urls import patterns, include, url
from mainapp.views import *

urlpatterns = [
    url(r'^newsfeed', newsfeed),
    url(r'^status', status),
    url(r'^profile', profile),
    url(r'^login', login_do),
    url(r'^logout', logout_do),
    url(r'^signup', signup),
    url(r'^comment', comment),
    url(r'^likestatus', like_status),
    url(r'^search', search),
    url(r'^', login_do),
    
]