from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Subject(models.Model):
    subject = models.CharField(max_length=50)
    active = models.CharField(max_length=1, default='Y')
    createdDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}: Subject: {self.subject} Active: {self.active} createdDate: {self.createdDate}"

class Tutor(models.Model):
    userstamp = models.CharField(max_length=32)
    image = models.CharField(max_length=200, null=True)
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    about = models.CharField(max_length=300)
    subject = models.CharField(max_length=64)
    grades = models.CharField(max_length=64)
    availability = models.CharField(max_length=200)
    createdDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, default='Requested')
    def __str__(self):
        return f"{self.id}: userstamp: {self.userstamp} image: {self.image} firstName: {self.firstName} lastName: {self.lastName} email: {self.email} about: {self.about} subject: {self.subject} grades: {self.grades} availability: {self.availability} createdDate: {self.createdDate} status: {self.status}"

class TutorSubject(models.Model):
    tutorid = models.IntegerField(default = 0)
    subject = models.CharField(max_length=64)
    active = models.CharField(max_length=1, default='Y')
    createdDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}: tutorid: {self.tutorid} subject: {self.subject} active: {self.active} createdDate: {self.createdDate}"

class Request(models.Model):
    description = models.CharField(max_length=200)
    subject = models.CharField(max_length=64)
    grade = models.CharField(max_length=32, default='None')
    availability = models.CharField(max_length=200)
    status = models.CharField(max_length=32, default='Requested')
    type = models.CharField(max_length=32)
    requestor = models.CharField(max_length=32)
    req_email = models.CharField(max_length=64, default='None')
    tutorname = models.CharField(max_length=32, default='None')
    tutoremail = models.CharField(max_length=64, default='None')
    userstamp = models.CharField(max_length=32, default='None')
    createdDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}: description: {self.description} subject: {self.subject} grade: {self.grade} avaliabililty: {self.availability} status: {self.status} type: {self.type} requestor: {self.requestor} req_email: {self.req_email} tutorname: {self.tutorname} tutoremail: {self.tutoremail} userstamp: {self.userstamp} createdDate: {self.createdDate}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    slug = models.SlugField()
    def __str__(self):
        return f"{self.id}: name: {self.name} price: {self.price} description: {self.description} slug: {self.slug}"

class CartItem(models.Model):
    cart_id = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return "{}:{}".format(self.product.name, self.id)
    
    def __str__(self):
        return f"{self.id}: cart_id: {self.cart_id} price: {self.price} quantity: {self.quantity} date_added: {self.date_added} product: {self.product}"

    def update_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    def total_cost(self):
        return self.quantity * self.price

class Order(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    postal_code = models.IntegerField()
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.id} name: {self.name} email: {self.email} postal_code: {self.postal_code} address: {self.address} date: {self.date} paid: {self.paid}"
    
    def total_cost(self):
        return sum([ li.cost() for li in self.lineitem_set.all() ])

class LineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id} order: {self.order} product: {self.product} price: {self.price} quantity: {self.quantity} date_added: {self.date_added}"

    def cost(self):
        return self.price * self.quantity
