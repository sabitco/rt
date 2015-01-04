from django.conf.urls import patterns, include, url
from django.conf import settings
from rtuit.views import TrendListView

urlpatterns = patterns('',
	url(r'^$', TrendListView.as_view(), name='list'),
    url(r'^rtuit/', include('rtuit.urls'))
)


