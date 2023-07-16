from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=20)

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    starting_bid = models.IntegerField()
    current_bid = models.IntegerField(default=starting_bid)
    starttime = models.DateTimeField(auto_now_add=True)
    endtime = models.DateTimeField()

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE)
    content = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now_add=True)
    
    