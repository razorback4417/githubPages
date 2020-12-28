from django.contrib import admin
from .models import Subject, Tutor, TutorSubject, Request
from .models import Product, CartItem, Order, LineItem

# Register your models here.

admin.site.register(Subject)
admin.site.register(Tutor)

admin.site.register(TutorSubject)
admin.site.register(Request)

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(LineItem)
