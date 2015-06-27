from django.conf.urls import patterns, include, url
from django.conf import settings
from rtuit.views import TrendListView
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^$', TrendListView.as_view(), name='list'),
    url(r'^rtuit/', include('rtuit.urls')),
    url(r'^admin/', include(admin.site.urls)),
)




