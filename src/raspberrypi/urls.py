from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import view

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'raspberrypi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^webcam/', include(view.CamView.as_view()))
)
