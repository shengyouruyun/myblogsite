from django.conf.urls import url
#from . import views
from blog.views import post_list, post_details, post_share
urlpatterns = [
# post views
url(r'^tag/(?P<tag_slug>[-\w]+)/$', post_list, name='post_list_by_tag'),

url(r'^(?P<post>[-\w]+)/$', 
	post_details, name='post_details'),

url(r'^(?P<post_id>\d+)/share/$', post_share, name='post_share'),
url(r'^$', post_list, name='post_list'),
]