from gamepanel import views

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    '',
    # /
    url(r'^$', views.home, name='home'),

    # /about/
    url(r'^about/$', views.about, name='about'),

    # /create/
    url(r'^create/$', views.create, name='create'),

    # /create/id
    url(r'^create/(?P<game_id>[0-9]+)/$', views.create_game, name='create_game'),

    # /server/id/pass/
    url(r'^server/(?P<id>[0-9]+)/(?P<password>[0-9]+)/$', views.created_server, name='created_server'),

    # /server/id/pass/command
    url(r'^server/(?P<id>[0-9]+)/(?P<password>[0-9]+)/(?P<command>[\w-]+)/$', views.command, name='command'),
)
