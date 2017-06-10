from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index),
    url(r'^regist$', views.regist),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^add_list/(?P<quote_id>\d+)$', views.add_list),
    url(r'^remove/(?P<quote_id>\d+)$', views.remove),
    url(r'^users/(?P<user_id>\d+)$', views.show),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
]
