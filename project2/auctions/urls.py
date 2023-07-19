from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("placebid", views.placebid, name="placebid"),
    path("addtowatchlist", views.addtowatchlist, name="addtowatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category_id>", views.category, name="category"),
    path("close", views.close, name="close"),
    path("<str:string>", views.error)
]
