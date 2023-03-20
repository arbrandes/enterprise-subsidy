"""
enterprise_subsidy URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

import os

from auth_backends.urls import oauth2_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.urls import include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from enterprise_subsidy.apps.api import urls as api_urls
from enterprise_subsidy.apps.core import views as core_views

admin.autodiscover()

schema_view = get_schema_view(
   openapi.Info(
      title="enterprise-subsidy API",
      default_version='v1',
      description="enterprise-subsidy API Docs",
   ),
   public=False,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = oauth2_urlpatterns + [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include(api_urls)),
    re_path(r'^api-docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api-docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^auto_auth/$', core_views.AutoAuth.as_view(), name='auto_auth'),
    re_path(r'', include('csrf.urls')),  # Include csrf urls from edx-drf-extensions
    re_path(r'^health/$', core_views.health, name='health'),
]

if settings.DEBUG and os.environ.get('ENABLE_DJANGO_TOOLBAR', False):  # pragma: no cover
    # Disable pylint import error because we don't install django-debug-toolbar
    # for CI build
    import debug_toolbar  # pylint: disable=import-error,useless-suppression
    urlpatterns.append(re_path(r'^__debug__/', include(debug_toolbar.urls)))
