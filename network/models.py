from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    userstamp = models.CharField(max_length=32, default='none')
    content = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}: userstamp: {self.userstamp} content: {self.content} timestamp: {self.timestamp}"

class Like(models.Model):
    postID = models.IntegerField(default=0)
    userstamp = models.CharField(max_length=32, default='none')
    def __str__(self):
        return f"{self.id}: postID: {self.postID} userstamp: {self.userstamp}"

class Follower(models.Model):
    author = models.CharField(max_length=32)
    follower = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.id}: author: {self.author} follower: {self.follower}"
