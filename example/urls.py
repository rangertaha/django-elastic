# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin

from simpleapp import urls

admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(urls)),
]
