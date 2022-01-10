# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from app import views 

from django.conf import settings #add this
from django.conf.urls.static import static #add this
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [   
    path('backend/', admin.site.urls),          # Django admin route
    path("", include("authentication.urls")),   # Auth routes - login / register
    path("", include("app.urls")), # App routes
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
