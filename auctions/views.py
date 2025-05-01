from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import User, Listing, Comment, Bid, WatchList, Like, Category

# ---------- Index Page ----------
def index(request):
    listings = Listing.objects.filter(status=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

# ---------- Authentication ----------
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        user_type = request.POST.get("user_type", "bidder")
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.user_type = user_type
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/register.html", {
        "user_types": User.USER_TYPE_CHOICES
    })

# ---------- Won Auctions View ----------
@login_required
def won_auctions(request):
    listings = Listing.objects.filter(winner=request.user, status=False)
    return render(request, "auctions/won_auctions.html", {
        "listings": listings
    })

# ---------- Listing Creation ----------
def create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
        
    if request.user.user_type not in ['seller', 'both']:
        return render(request, "auctions/create.html", {
            "message": "Only sellers can create listings. Please update your account type.",
            "categories": Category.objects.all()
        })
        
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all()
        })
    else:
        try:
            title = request.POST['title']
            description = request.POST['description']
            starting_price = float(request.POST['price'])
            image = request.POST.get('image', '')
            category_id = request.POST.get('category')
            end_date = request.POST.get('end_date')
            
            category = None
            if category_id:
                category = Category.objects.get(id=category_id)
                
            listing = Listing.objects.create(
                title=title,
                description=description,
                starting_price=starting_price,
                current_price=starting_price,
                image_url=image,
                category=category,
                seller=request.user,
                end_date=end_date if end_date else None
            )
            
            return HttpResponseRedirect(reverse("index"))
            
        except Exception as e:
            return render(request, "auctions/create.html", {
                "message": str(e),
                "categories": Category.objects.all()
            })

# ---------- Category Creation ----------
@require_POST
@login_required
def create_category(request):
    name = request.POST.get('name')
    description = request.POST.get('description')

    if not name:
        return JsonResponse({
            'success': False,
            'error': 'Category name is required'
        })

    try:
        category = Category.objects.create(name=name, description=description)
        return JsonResponse({
            'success': True,
            'id': category.id,
            'name': category.name
        })
    except IntegrityError:
        return JsonResponse({
            'success': False,
            'error': 'Category already exists'
        })

# ---------- Interactive Actions (AJAX) ----------
@require_POST
@login_required
def like(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    like, created = Like.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        like.delete()
    return JsonResponse({
        'liked': created,
        'likes_count': listing.likes.count()
    })


@require_POST
@login_required
def comment(request, title):
    listing = get_object_or_404(Listing, title=title)
    comment_text = request.POST.get('comment')

    if not comment_text:
        return JsonResponse({'error': 'Comment cannot be empty'}, status=400)

    Comment.objects.create(
        writer=request.user,
        product=listing,
        comment=comment_text
    )
    return JsonResponse({
        'username': request.user.username,
        'comment': comment_text
    })


@require_POST
@login_required
def bid(request, item):
    listing = get_object_or_404(Listing, title=item)
    
    if not listing.is_active():
        return JsonResponse({
            'success': False,
            'message': 'This auction has ended'
        }, status=400)
    
    try:
        bid_amount = request.POST.get('bid')
        if not bid_amount:
            return JsonResponse({
                'success': False,
                'message': 'Bid amount is required'
            }, status=400)
            
        try:
            bid_amount = float(bid_amount)
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'message': 'Invalid bid amount'
            }, status=400)
            
        if bid_amount <= listing.current_price:
            return JsonResponse({
                'success': False,
                'message': f'Bid must be greater than current price (${listing.current_price})'
            }, status=400)

        Bid.objects.create(
            listing=listing,
            bidder=request.user,
            price=bid_amount
        )
        
        listing.current_price = bid_amount
        listing.save()

        return JsonResponse({
            'success': True,
            'new_price': listing.current_price,
            'bid_count': Bid.objects.filter(listing=listing).count(),
            'message': 'Your bid is the current bid'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@require_POST
@login_required
def watch(request, title):
    listing = get_object_or_404(Listing, title=title)
    watchlist, created = WatchList.objects.get_or_create(user=request.user, item=listing)
    if not created:
        watchlist.delete()
    return JsonResponse({'watchlist': created})

# ---------- Listing View ----------
def listing_page(request, title):
    listing = get_object_or_404(Listing, title=title)
    bids = Bid.objects.filter(listing=listing)
    comments = Comment.objects.filter(product=listing)
    watch = False
    condition = False
    is_active = listing.is_active()

    if request.user.is_authenticated:
        user = request.user
        watch = WatchList.objects.filter(user=user, item=listing).exists()
        condition = bids.filter(bidder=user).exists()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids.count(),
        "comments": comments,
        "watch": watch,
        "condition": condition,
        "is_active": is_active,
        "time_remaining": listing.end_date - timezone.now() if is_active else None
    })

# ---------- Watchlist View ----------
@login_required
def watchlist(request):
    watchlist_items = WatchList.objects.filter(user=request.user)
    listings = [item.item for item in watchlist_items]
    return render(request, 'auctions/watch.html', {
        "listings": listings
    })

# ---------- Category Views ----------
def category(request):
    return render(request, 'auctions/category.html', {
        "categories": Category.objects.all()
    })

def category_listings(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    listings = Listing.objects.filter(category=category, status=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "category": category
    })

# ---------- Close Auction ----------
@login_required
def close(request, title):
    listing = get_object_or_404(Listing, title=title)
    listing.close_auction()
    return HttpResponseRedirect(reverse("index"))
