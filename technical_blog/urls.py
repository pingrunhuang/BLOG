from django.conf.urls import url
from technical_blog import views
urlpatterns = [
	url(r'^$', views.post_list, name='technical_post_list'),
	url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='technical_post_detail')
]
