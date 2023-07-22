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
    path("comment", views.comment, name="comment"),
    
    #admin
    path("admin_listings", views.admin_listings, name="admin_listings"),
    path("admin_comments", views.admin_comments, name="admin_comments"),
    path("admin_bids", views.admin_bids, name="admin_bids"),
    path("deletecomment/<int:comment_id>", views.delete_comment),
    path("deletebid/<int:bid_id>", views.delete_bid),
    path("editlisting/<int:listing_id>", views.edit_listing),
    path("deletelisting/<int:listing_id>", views.delete_listing),
    path("confirmedit", views.confirm_edit, name='confirm_edit'),
    path("createcategory", views.create_category, name="create_category"),

    #erro
    path("<str:string>", views.error)
]
