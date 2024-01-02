from django.urls import include, path

urlpatterns = [
    # ratings
    path("ratings/", include("star_ratings.urls", namespace="ratings")),
]
