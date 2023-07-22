from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User

from django import forms

from auctions.models import Category, Listing, Bid, User, Watchlist, Winner, Comment


def index(request):
    if request.user.is_superuser:
        return render(request, "admin/index.html", {
            'listings' : Listing.objects.all()
        })
    else:
        return render(request, "auctions/index.html", {
            "listings" : Listing.objects.all()
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


class CreateListing(forms.Form):
    title = forms.CharField(max_length=20)
    description = forms.CharField(widget=forms.Textarea(attrs={"maxlength":"200", "columns":"10"}))
    bid = forms.FloatField(min_value=0.01)
    image = forms.URLField()
    category = forms.ChoiceField(choices=[(cat.id, cat.name) for cat in Category.objects.all()])


def create(request):
    if request.method == 'POST':
        create = CreateListing(request.POST)
        if create.is_valid():
            data = create.cleaned_data
            listing = Listing(user = User.objects.get(username = request.user.username), 
                              title = data['title'], 
                              description = data['description'],
                              image = data['image'],
                              category = Category.objects.get(id = int(data['category'])),
                              starting_bid = float(data['bid']),
                              current_bid = float(data['bid']),
                              )
            listing.save()
            Bid(user = User.objects.get(username = request.user.username), listing = listing, amount = float(data['bid'])).save()
            return redirect("index")          
    return render(request, "auctions/create.html", {
        "create": CreateListing()
    })      

def listing(request, listing_id):
    listing = Listing.objects.filter(id = listing_id)
    winner = None
    if len(Winner.objects.filter(listing = listing[0])) > 0:
        winner = Winner.objects.filter(listing = listing[0])[0].user
    if len(listing) == 0:
        return redirect("index")
    return render(request, "auctions/listing.html",{
        "listing" : listing[0],
        "n_bids": len(Bid.objects.filter(listing = listing[0])),
        "top_bidder" : Bid.objects.filter(amount = listing[0].current_bid)[0].user.id,
        "min" : listing[0].current_bid + 0.01,
        "watchlist" : len(Watchlist.objects.filter(user = User.objects.get(id=request.user.id), listing = listing[0])) > 0,
        "open" : listing[0].open,
        "winner" : winner,
        "comments" : Comment.objects.filter(listing = listing[0])
    })
    
def placebid(request):
    if request.method == 'POST':
        data = request.POST
        
        user = User.objects.get(id = data['user_id'])
        listing = Listing.objects.get(id = data['listing_id'])
        amount = float(data['amount'])
        
        if amount > listing.current_bid:
            Bid(user = user, listing = listing, amount = amount).save()
            listing.current_bid = amount
            listing.save()

    return redirect("listing", listing_id = data['listing_id'])
    
def addtowatchlist(request):
    if request.method == 'POST':
        data = request.POST

        user = User.objects.get(id = data['user_id'])
        listing = Listing.objects.get(id = data['listing_id'])

        if len(Watchlist.objects.filter(user = user, listing = listing)) > 0:
            Watchlist.objects.filter(user = user, listing = listing)[0].delete()
        
        else:
            Watchlist(user = user, listing = listing).save()
    
    return redirect("listing", listing_id = data['listing_id'])

def watchlist(request):
    watchlist = Watchlist.objects.filter(user = User.objects.get(id = request.user.id))
    return render(request, "auctions/watchlist.html", {
        'listings' : [w.listing for w in watchlist]
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories" : Category.objects.all()
    })

def category(request, category_id):
    category = Category.objects.filter(id = category_id)
    if len(category) == 0:
        return redirect("index")
    return render(request, "auctions/category.html",{
        "category" : category[0],
        "listings" : Listing.objects.filter(category = category[0])
    })

def error(request, string):
    return redirect("index")

def addtowatchlist(request):
    if request.method == 'POST':
        data = request.POST

        user = User.objects.get(id = data['user_id'])
        listing = Listing.objects.get(id = data['listing_id'])

        if len(Watchlist.objects.filter(user = user, listing = listing)) > 0:
            Watchlist.objects.filter(user = user, listing = listing)[0].delete()
        
        else:
            Watchlist(user = user, listing = listing).save()
    
    return redirect("listing", listing_id = data['listing_id'])

def close(request):
    if request.method == 'POST':
        data = request.POST

        listing = Listing.objects.get(id = data['listing_id'])
        bid = Bid.objects.get(listing = listing, amount = listing.current_bid)

        winner = Winner(user = bid.user, listing = listing)
        listing.open = False
        listing.save()
        winner.save()
    
    return redirect("listing", listing_id = data['listing_id'])

def comment(request):
    if request.method == 'POST':
        data = request.POST

        listing = Listing.objects.get(id = data['listing_id'])
        user = User.objects.get(id = data['user_id'])
        title = data['title']
        content = data['content']

        Comment(listing = listing, user = user, title = title, content = content).save()

    return redirect("listing", listing_id = data['listing_id'])



def admin_listings(request):
    return render(request, "admin/listings.html", {
        "listings" : Listing.objects.all()
    })

def admin_comments(request):
    return render(request, "admin/comments.html", {
        "comments": Comment.objects.all()
    })

def admin_bids(request):
    return render(request, "admin/bids.html", {
        "bids" : Bid.objects.all()
    })

def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('admin_comments')

def delete_bid(request, bid_id):
    bid = Bid.objects.get(id=bid_id)
    bids = [a.amount for a in Bid.objects.filter(listing = bid.listing)]
    if len(bids) > 1:
        bid.delete()
        listing = bid.listing
        listing.current_bid = max([a.amount for a in Bid.objects.filter(listing = listing)])
        listing.save()
    return redirect('admin_bids')

def edit_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, "admin/editlisting.html",{
        "listing" : listing,
        "categories" : Category.objects.all()
    })
def confirm_edit(request):
    if request.method == 'POST':
        data = request.POST
        listing = Listing.objects.get(id=data['listing_id'])
        listing.title = data['title']
        listing.description = data['description']
        listing.category = Category.objects.get(name=data['category'])
        listing.save()
        return redirect("listing", listing_id = int(data['listing_id']))

def delete_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    for comment in Comment.objects.get(listing=listing):
        comment.delete()
    for bid in Bid.objects.get(listing = listing):
        bid.delete()
    for winner in Winner.objects.get(listing = listing):
        winner.delete()
    listing.delete()
    return redirect("index")

def create_category(request):
    if request.method == 'POST':
        data = request.POST

        Category(name=data['name']).save()

        return redirect('categories')