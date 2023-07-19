from django.contrib.auth.models import AbstractUser
from django.db import models

import datetime


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=20)

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    image = models.URLField(default="https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    starting_bid = models.FloatField()
    current_bid = models.FloatField(default=starting_bid)
    start = models.DateTimeField(default=datetime.datetime.now())
    open = models.BooleanField(default=True)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.FloatField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE)
    content = models.CharField(max_length=200)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Winner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)