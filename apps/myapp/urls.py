from django.conf.urls import url 
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^create$', views.create),
	url(r'^login$',views.login),
	url(r'^logged$', views.logged),
	url(r'^addplan$', views.addplan),
	url(r'^maketrip$', views.maketrip),
	url(r'^destination/(?P<tripid>\d+)$', views.destination),
	url(r'^join/(?P<tripid>\d+)$', views.join)
	]