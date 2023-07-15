from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name = "search"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("newpage", views.newpage, name="newpage"),
    path("random", views.random, name="random"),
    path("editpage/<str:title>", views.editpage, name="editpage")
]
