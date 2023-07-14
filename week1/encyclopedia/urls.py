from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki),
    path("search", views.search, name = "search"),
    path("newpage", views.newpage, name="newpage")
]
