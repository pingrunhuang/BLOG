from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.post_list, name='life_post_list'),
	url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='life_post_detail')
]
