from django.urls import path

from . import views

urlpatterns = [
    # Main pages
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("won_auctions", views.won_auctions, name="won_auctions"),
    path("category", views.category, name="category"),
    path("category/<int:category_id>", views.category_listings, name="category_listings"),
    
    # Listing related
    path("create", views.create, name="create"),
    path("listing/<int:id>", views.listing_page, name="listing"), # jugeer/hyt
    path("close/<int:id>", views.close, name="close"),
    
    # AJAX endpoints
    path("watch/<int:id>", views.watch, name="watch"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("like/<int:listing_id>", views.like, name="like"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("create_category", views.create_category, name="create_category"),
]
