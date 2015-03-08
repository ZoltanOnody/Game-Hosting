from blog import views

from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'gameserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # /
    url(r'^$', views.home, name='home'),

    # /category/category-name/
    url(r'^category/(?P<slug>[\w-]+)/$', views.category, name='category'),

    # /tag/tag-name/
    url(r'^tag/(?P<slug>[\w-]+)/$', views.tag, name='tag'),

    # /this-is-article/
    url(r'(?P<slug>[\w-]+)/$', views.single, name='single'),
)
