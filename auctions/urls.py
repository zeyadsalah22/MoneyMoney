from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create , name="create"),
    path("listing/<str:title>" , views.listing_page, name='listing_page'),
    path("bid/<str:item>", views.bid, name="bid"),
    path("watch/<str:title>", views.watch , name="watch"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("close/<str:title>", views.close,name="close"),
    path("categories/", views.category, name="category"),
    path("category_listings/<str:category>", views.category_listings, name="category_listings")
]
