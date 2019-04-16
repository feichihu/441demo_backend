"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from user import views
# from chatter import views

urlpatterns = [
    # url(r'^getchatts/$', views.getchatts, name='getchatts'),
	# url(r'^addchatt/$', views.addchatt, name='addchatt'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.getuser, name='getuser'),
    url(r'^searchuser/$', views.searchuser, name='searchuser'),
    url(r'^leaderboard/(?P<user_id>[0-9]+)/$', views.getleaderboard, name='getleaderboard'),
    url(r'^adduser/$', views.adduser, name='adduser'),
    url(r'^updatename/$', views.updatename, name='updatename'),
    url(r'^addfriend/$', views.addfriend, name='addfriend'),
    url(r'^deletepending/$', views.delete_pending, name='deletepending'),
    url(r'^getpending/(?P<user_id>[0-9]+)/$', views.getpending, name='getpending'),
    url(r'^updatescore/$', views.update_all, name='updatescore'),
    url(r'^updatelink/$', views.Update_Link, name='updatelink'),
    url(r'^searchsong/$', views.Search_song, name='searchsong'),
    url(r'^addpending/$', views.addpending, name='addpending'),
    url(r'^profile/friends/(?P<user_id>[0-9]+)/$', views.getfriends, name='getfriends'),
    url(r'^admin/', include(admin.site.urls)),
]

