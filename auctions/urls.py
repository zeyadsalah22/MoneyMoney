from django.urls import path

from . import views

urlpatterns = [
    # Main pages
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name="category"),
    path("category/<int:category_id>", views.category_listings, name="category_listings"),
    
    # Listing related
    path("create", views.create, name="create"),
    path("listing/<str:title>", views.listing_page, name="listing_page"),
    path("close/<str:title>", views.close, name="close"),
    
    # AJAX endpoints
    path("watch/<str:title>", views.watch, name="watch"),
    path("bid/<str:item>", views.bid, name="bid"),
    path("like/<int:listing_id>", views.like, name="like"),
    path("comment/<str:title>", views.comment, name="comment"),
    path("category/create", views.create_category, name="create_category"),
]
