"""Notar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$',
        views.Home.as_view(),
        name='home'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^(?P<url>[-\w/]+)/$',
        views.FlatPageView.as_view(),
        name='flatpage'),
]

# This line does only work during development (settings.DEBUG == True)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
