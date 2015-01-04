from django.conf.urls import patterns, url
from rtuit.views import TrendCreateView, TrendDetailView, TrendUpdateView, TrendDeleteView
from rtuit.views import TrendSummaryView
from rtuit.views import TrendInfoView

urlpatterns = patterns('',
    url(r'^add/$', TrendCreateView.as_view(), name='create'),
    url(r'^informacion/$', TrendInfoView.as_view(), name='informacion'),
	url(r'^(?P<pk>[\w\d]+)/summary/$', TrendSummaryView.as_view(), name='summary'),
    url(r'^(?P<pk>[\w\d]+)/$', TrendDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[\w\d]+)/edit/$', TrendUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[\w\d]+)/delete/$', TrendDeleteView.as_view(), name='delete'),
)

