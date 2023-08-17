from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Listing,Comment,Bid,WatchList


def index(request):
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.filter(status="active")
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method=="GET":
        return render(request,"auctions/create.html",{
        })
    else:
        title = request.POST['title']
        description = request.POST['description']
        price = float(request.POST['price'])
        image = request.POST['image']
        category = request.POST['category']
        item = Listing.objects.create(title=title,description=description, current_price=price, category=category, image_url = image,seller=request.user)    
        item.save()
        return HttpResponseRedirect(reverse("index"))

def listing_page(request,title):
    listing = Listing.objects.get(title=title)
    bids = Bid.objects.filter(listing=listing)
    comments = Comment.objects.filter(product=listing)
    if request.method=="POST":
        comment = request.POST['comment']
        new_comment = Comment.objects.create(comment=comment,product=listing,writer=request.user)
        new_comment.save()
        comments = Comment.objects.filter(product=listing)
    if request.user.is_authenticated:
        user = request.user
    else:
        user=None 
    return render(request,"auctions/listing.html",{
        "listing":listing,
        "bids": bids.count(),
        "comments":comments,
        "condition": Bid.objects.filter(listing=listing,price=listing.current_price,bidder=user),
        "watch": WatchList.objects.filter(user=user ,item=listing)
    })

def bid(request,item):
    if request.method=="POST":
        listing = Listing.objects.get(title=item)
        bids = Bid.objects.filter(listing=listing)
        comments = Comment.objects.filter(product=listing)
        price = float(request.POST['bid'])
        if price<=listing.current_price and not (price>=listing.current_price and bids.count()==0):
            return render(request,'auctions/listing.html',{
                "listing":listing,
                "bids": bids.count(),
                "condition": Bid.objects.filter(listing=listing,price=listing.current_price,bidder=request.user),
                "message": "your bid must be greater than the current price",
                "comments":comments,
                "watch": WatchList.objects.filter(user=request.user,item=listing)
            })
        else:
            new_bid = Bid.objects.create(bidder=request.user,listing=listing,price=price)
            new_bid.save()
            listing.current_price=price
            listing.save()
            return render(request,'auctions/listing.html',{
                "listing":listing,
                "bids": bids.count(),
                "condition": Bid.objects.filter(listing=listing,price=listing.current_price,bidder=request.user),
                "message": "Your bid has been placed successfully",
                "comments":comments,
                "watch": WatchList.objects.filter(user=request.user,item=listing)
            })

def watch(request,title):
    listing = Listing.objects.get(title=title)
    bids = Bid.objects.filter(listing=listing)
    comments = Comment.objects.filter(product=listing)
    if request.method=='POST':
        watchlist = request.POST['watchlist']
        if watchlist=='+':
            new_watch = WatchList.objects.create(item=listing,user=request.user)
            new_watch.save()
        else:
            removed_watch = WatchList.objects.filter(item=listing,user=request.user)
            removed_watch.delete()
        return render(request,"auctions/listing.html",{
            "listing":listing,
            "bids": bids.count(),
            "comments":comments,
            "condition": Bid.objects.filter(listing=listing,price=listing.current_price,bidder=request.user),
            "watch": WatchList.objects.filter(user=request.user,item=listing)
        })


def watchlist(request):
    list = WatchList.objects.filter(user=request.user)
    listings = []
    for i in list:
        listings.append(i.item)
    return render(request,'auctions/watch.html',{
        "listings":listings
    })

def close(request,title):
    listing = Listing.objects.get(title=title)
    listing.status="closed"
    listing.save()
    return render(request,'auctions/index.html',{
        "listings":Listing.objects.filter(status="active")
    })

def category(request):
    listings = Listing.objects.all()
    categories = []
    for listing in listings:
        if listing.category not in categories and listing.category:
            categories.append(listing.category)
    return render(request,'auctions/category.html',{
        "categories":categories
    })

def category_listings(request,category):
    listings = Listing.objects.filter(category=category)
    return render(request,"auctions/index.html",{
        "listings":listings
    })