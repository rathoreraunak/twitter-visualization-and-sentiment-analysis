from django.conf.urls import url
from . import views
from .views import userinput

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^analyse/$', views.analyse, name='analyse'),
    url(r'^analysesingle/$', views.analyseSingle, name='analysesingle'),
    url(r'^analysesingle_user/$', views.analysesingle_user, name='analysesingle_user'),
    url(r'^trends/$', views.getTrends, name='trends'),
    url(r'^getWoeid/$', views.getWoeidView, name='getPlacesID'),
    url(r'^getTrendsTwitter/(?P<woeid>\d+)$', views.getCurrentTrends, name='getCurrentTrends'),
]