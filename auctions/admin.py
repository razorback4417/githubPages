from django.contrib import admin
from .models import Bid, Comment, Listing, Watchlist

# Register your models here.
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(Watchlist)



