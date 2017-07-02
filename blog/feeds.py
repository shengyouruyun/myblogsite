from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

class LatestPostsFeed(Feed):
	title = 'My blog'
	link = '/blog/'
	description = 'New posts of my blog.'
	print title
	print Post.objects.all()

	def items(self):
		return Post.objects.all()[:2]
	def item_title(self, item):
		return item.title
	def item_description(self, item):
		return truncatewords(item.body, 20)