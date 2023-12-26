import importlib
import os

from auth_backends.urls import oauth2_urlpatterns
from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from edx_operation.apps.api import urls as api_urls
from edx_operation.apps.core import views as core_views

admin.autodiscover()

urlpatterns = oauth2_urlpatterns + [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^auto_auth/$", core_views.AutoAuth.as_view(), name="auto_auth"),
    re_path(r"", include("csrf.urls")),  # Include csrf urls from edx-drf-extensions
    re_path(r"^health/$", core_views.health, name="health"),
]


# all app's urls
for app_config in apps.get_app_configs():
    app_name = app_config.name
    if not app_name.startswith("edx_operation.apps"):
        continue

    # Dynamically import the urls module
    try:
        urls_module = importlib.import_module(f"{app_name}.urls", package=app_name)
    except ModuleNotFoundError:
        continue

    if hasattr(urls_module, "urlpatterns"):
        urlpatterns.append(path("", include(f"{app_name}.urls")))


if settings.DEBUG and os.environ.get("ENABLE_DJANGO_TOOLBAR", False):  # pragma: no cover
    # Disable pylint import error because we don't install django-debug-toolbar
    # for CI build
    import debug_toolbar  # pylint: disable=import-error

    urlpatterns.append(re_path(r"^__debug__/", include(debug_toolbar.urls)))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
