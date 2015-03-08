from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.conf.urls.static import static


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'gameserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^redactor/', include('redactor.urls')),
    url(r'^captcha/', include('captcha.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'', include('gamepanel.urls', namespace='gamepanel')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
