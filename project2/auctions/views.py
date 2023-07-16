from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User

from django import forms

from auctions.models import Category, Listing


def index(request):
    return render(request, "auctions/index.html")


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
    description = forms.CharField(max_length=200)
    bid = forms.IntegerField(min_value=0)
    image = forms.URLField()
    category = forms.ChoiceField(choices=[(cat.id, cat.name) for cat in Category.objects.all()])


def create(request):
    if request.method == 'POST':
        create = CreateListing(request.POST)
        if create.is_valid():
            data = create.cleaned_data
            category = Category(name="teste")
            category.save()
            listing = Listing(user = User.objects.get(username = request.user.username), 
                              title = data['title'], 
                              description = data['description'],
                              image = data['image'],
                              category = Category.objects.get(id = int(data['category'])),
                              starting_bid = int(data['bid']),
                              current_bid = int(data['bid']),
                              )
            listing.save()
            return redirect("index")          
    return render(request, "auctions/create.html", {
        "create": CreateListing()
    })