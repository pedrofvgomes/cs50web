
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("like/<int:post_id>", views.like, name="like"),
    path('follow/<str:username>', views.follow),
    path('following', views.following),
    path('edit/<int:post_id>/<str:body>', views.edit),
    path('<str:username>', views.profile, name="profile")
]
