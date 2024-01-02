from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    # comments
    path("comments/", include("django_comments_xtd.urls")),
    path(r"jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
]
