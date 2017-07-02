from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap 
from blog.feeds import LatestPostsFeed
sitemaps = {
'posts': PostSitemap,
}

feed = LatestPostsFeed()
admin.autodiscover()
urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^blog/', include('blog.urls',
								namespace='blog',
								app_name='blog')),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
name='django.contrib.sitemaps.views.sitemap'),

    url(r'^blog/feed\.xml$', feed, name='post_feed'),
]
