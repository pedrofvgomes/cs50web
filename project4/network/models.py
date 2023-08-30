from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# user 1 follows user 2
# when they are mutuals, there will be 2 Following objects - user1-user2 and user2-user1
class Following(models.Model):
    user1 = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user2")

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    body = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

class Liked(models.Model):
    user = models.ForeignKey("User", on_delete= models.CASCADE)
    post = models.ForeignKey("Post", on_delete= models.CASCADE)
