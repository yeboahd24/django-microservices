from django.urls import path
from userpost.api_views.post import post


urlpatterns = [
    path("create/", post, name="post"),
]
