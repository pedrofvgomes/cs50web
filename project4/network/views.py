from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Liked, Following


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "page_posts": page_posts
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def newpost(request):
    if request.method == 'POST':
        data = request.POST
        user = User.objects.get(username = data['username'])
        body = data['text']

        newpost = Post(user = user, body = body)
        newpost.save()
        return redirect("index")
    else:
        return render(request, "network/index.html")
    
def like(request, post_id):
    if not request.user.username:
        return JsonResponse('', safe=False)
    post = Post.objects.get(id = post_id)

    # remove like
    if len(Liked.objects.filter(post = post, user=request.user)):
        Liked.objects.get(post = post).delete()
        post.likes -= 1
        post.save()
        return JsonResponse("Removed", safe=False)
    else:
        Liked(user = request.user, post = post).save()
        post.likes += 1
        post.save()
        return JsonResponse("Added", safe=False)
    
def profile(request, username):
    if len(User.objects.filter(username=username)) == 0:
        return redirect('index')
    user = User.objects.get(username=username)
    follows = False
    if request.user.is_authenticated:
        if len(Following.objects.filter(user1=request.user, user2=user)): 
            follows = True
    posts = Post.objects.filter(user=user).order_by("-timestamp")
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "userprofile": user,
        "followers": len(Following.objects.filter(user2=user)),
        "following": len(Following.objects.filter(user1=user)),
        "page_posts": page_posts,
        "follows": follows
    })
    
def follow(request, username):
    # user doesnt exist
    if len(User.objects.filter(username = username)) == 0:
        return redirect('index')
    user = User.objects.get(username = username)
    if len(Following.objects.filter(user1 = request.user, user2 = user)) == 0:
        Following(user1 = request.user, user2 = user).save()
    else:
        Following.objects.get(user1 = request.user, user2 = user).delete()
    
    return redirect("profile", username = username)

def following(request):
    if not request.user.is_authenticated:
        return redirect('index')
    posts = []
    for user in [following.user2 for following in Following.objects.filter(user1 = request.user)]:
        posts += Post.objects.filter(user = user)
    return render(request, 'network/following.html', {
        "posts" : posts
    })

def edit(request, post_id, body):
    post = Post.objects.filter(id = post_id)
    if len(post) == 0:
        return redirect('index')
    post = post[0]
    if request.user != post.user:
        return redirect('index')
    post.body = body
    post.save()
    return HttpResponse(status = 204)
    