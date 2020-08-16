from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    image = models.CharField(max_length=128, null=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=64, default='No Category Listed')
    userstamp = models.CharField(max_length=32)
    createdDate = models.DateTimeField(auto_now_add=True)
    active = models.CharField(max_length=1, default='Y')
    def __str__(self):
        return f"{self.id}:Title: {self.title} Description: {self.description} Price: {self.price} Category: {self.category} Userstamp: {self.userstamp} createdDate: {self.createdDate} Active: {self.active}"

class Bid(models.Model):
    title = models.CharField(max_length=64)
    prodid = models.IntegerField(default=0) 
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    userstamp = models.CharField(max_length=32)
    createdDate = models.DateTimeField(auto_now_add=True)
    win = models.CharField(max_length=1, default='N')
    def __str__(self):
        return f"{self.id}:Title: {self.title} ProductId: {self.prodid} Bid: {self.bid} Userstamp: {self.userstamp} createdDate: {self.createdDate} Win: {self.win}"

class Comment(models.Model):
    title = models.CharField(max_length=64)
    prodid = models.IntegerField(default=0)
    comment = models.CharField(max_length=512)
    userstamp = models.CharField(max_length=32)
    createdDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}:Title: {self.title} ProductId: {self.prodid} Comment: {self.comment} Userstamp: {self.userstamp} createdDate: {self.createdDate}"

class Watchlist(models.Model):
    title = models.CharField(max_length=64)
    prodid = models.IntegerField(default=0)
    userstamp = models.CharField(max_length=32)
    createdDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}:Title: {self.title} ProductID: {self.prodid} Userstamp: {self.userstamp} createdDate: {self.createdDate}"
