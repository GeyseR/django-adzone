from django.conf.urls import *

from adzone.views import ad_view

urlpatterns = patterns('',
    url(r'^view/(?P<id>[\d]+)/$', ad_view, name='adzone_ad_view'),
)
