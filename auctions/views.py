from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Listing, User, Bid, Comment, Watchlist

from django.db.models import Max, Q

def index(request):
    #index page from Active Listing or Categories?
    category = request.GET.get('value', 'index')

    if category == 'index':
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all(),
            "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count()
        })
    else:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(category=category),
            "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count()
        })

def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        descrip = request.POST.get('des')
        startBid = request.POST.get('sBid')
        category = request.POST.get('cat')
        image = request.POST.get('uI')
        userstamp = request.POST.get('userstamp')

        if category == "":
            category = "No Category Listed"

        try:
            listing = Listing(image=image, title=title, description=descrip, price=startBid, category=category, userstamp=userstamp)
            listing.save()
        except IntegrityError:
            return render(request, "auctions/create.html", {
                "message": "Listing already existed.",
                "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count()
            })
        return HttpResponseRedirect(reverse("create"))
    else:
        return render(request, "auctions/create.html", {
            "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count()
        })
    

def watchlist(request):
    # obtain all the listing IDs from the Watchlist table for the current login user
    watchlists = Watchlist.objects.filter(userstamp=request.user).values_list('prodid', flat=True)
    
    # set to empty query set
    listings = Listing.objects.filter(id=0)
    
    # build up all the records returned for a given listing ID
    if watchlists:
        for wl in watchlists:
            listings = listings.union(Listing.objects.filter(id=wl))

    return render(request, "auctions/watchlist.html", {
        "watchlists": listings,
        "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count()
    })

def listing(request, id):
    title = Listing.objects.values_list('title', flat=True).get(pk=id)
    price = Listing.objects.values_list('price', flat=True).get(pk=id)
    active = Listing.objects.values_list('active', flat=True).get(pk=id)
    currentBid = Bid.objects.filter(prodid=id).aggregate(Max('bid'))['bid__max']

    if active == 'N':
        winner = Bid.objects.filter(prodid=id, win='Y').values_list('userstamp', flat=True)[0]
    else:
        winner = 'None'
    
    if currentBid is None:
        currentBid = 0.0

    if price > currentBid:
        currentBid = price
        numBids = 0
        currentBidder = "None"
    else:
        numBids = Bid.objects.filter(prodid=id).count()
        currentBidder = Bid.objects.filter(prodid=id, bid=currentBid).values_list('userstamp', flat=True)[0]

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=id),
        "currentBid": currentBid,
        "currentBidder": currentBidder,
        "numBids": numBids,
        "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count(),
        "currentWLcount": Watchlist.objects.filter(userstamp=request.user, prodid=id).count(),
        "comments": Comment.objects.filter(prodid=id),
        "active": active,
        "winner": winner,
        "message": "None"
    }) 

def editListing(request):
    if request.method == "POST":

        id = request.POST['id']
        title = Listing.objects.values_list('title', flat=True).get(pk=id)
        bidder = request.POST['bidder']
        currentBid = request.POST['currentBid']
        currentBidder = request.POST['currentBidder']

        if request.POST.get("addcomment-btn"):
            comment = request.POST['entercomment']
            print('comment=', comment)
            commentObj = Comment(title=title, comment=comment, prodid=id, userstamp=bidder)
            commentObj.save()

            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(pk=id),
                "currentBid": request.POST['currentBid'],
                "currentBidder": bidder,
                "numBids": Bid.objects.filter(title=title).count(),
                "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count(),
                "currentWLcount": Watchlist.objects.filter(userstamp=request.user, prodid=id).count(),
                "comments": Comment.objects.filter(prodid=id)
            })

        if request.POST.get("closebid"):
            count = Bid.objects.filter(prodid=id).count()
            if count is None:
                count = 0
            if count != 0:
                #winner
                bid = Bid.objects.get(prodid=id, userstamp=currentBidder, bid=currentBid)
                bid.win = 'Y'
                bid.save()

                #make nonactive
                li = Listing.objects.get(id=id)
                li.active = 'N'
                li.save()

                return render(request, "auctions/index.html", {
                    "listings": Listing.objects.filter(),
                    "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count()
                 })
            else:
                return render(request, "auctions/listing.html", {
                    "listing": Listing.objects.get(pk=id),
                    "currentBid": request.POST['currentBid'],
                    "currentBidder": bidder,
                    "numBids": Bid.objects.filter(title=title).count(),
                    "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count(),
                    "message": "Error: Not available bid(s) to close."
                })       

        if request.POST.get("addwatchlist"):

            count = Watchlist.objects.filter(title=title, userstamp=bidder).count()
            if count is None:
                count = 0

            if count == 0:
                wl = Watchlist(title=title, prodid=id, userstamp=bidder)
                wl.save()

                return render(request, "auctions/listing.html", {
                    "listing": Listing.objects.get(pk=id),
                    "currentBid": request.POST['currentBid'],
                    "currentBidder": bidder,
                    "numBids": Bid.objects.filter(title=title).count(),
                    "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count(),
                    "currentWLcount": Watchlist.objects.filter(userstamp=request.user, prodid=id).count()
                 })
            
            else:
                return render(request, "auctions/listing.html", {
                    "listing": Listing.objects.get(pk=id),
                    "currentBid": request.POST['currentBid'],
                    "currentBidder": bidder,
                    "numBids": Bid.objects.filter(title=title).count(),
                    "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count(),
                    "currentWLcount": Watchlist.objects.filter(userstamp=request.user, prodid=id).count(),
                    "message": "Error: Watchlist already existed."
                })

        if request.POST.get("removewatchlist"):
            # bid in watchlist?
            count = Watchlist.objects.filter(prodid=id, userstamp=bidder).count()
            if count is None:
                count = 0

            if count > 0:
                wl = Watchlist.objects.get(title=title, prodid=id, userstamp=bidder)
                wl.delete()

                return render(request, "auctions/listing.html", {
                    "listing": Listing.objects.get(pk=id),
                    "currentBid": request.POST['currentBid'],
                    "currentBidder": bidder,
                    "numBids": Bid.objects.filter(prodid=id).count(),
                    "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count(),
                    "currentWLcount": Watchlist.objects.filter(userstamp=request.user, prodid=id).count()
                 })
            else:
                return render(request, "auctions/listing.html", {
                    "listing": Listing.objects.get(pk=id),
                    "currentBid": request.POST['currentBid'],
                    "currentBidder": bidder,
                    "numBids": Bid.objects.filter(title=title).count(),
                    "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count(),
                    "currentWLcount": Watchlist.objects.filter(userstamp=request.user, prodid=id).count(),
                    "message": "Error: Watchlist not existed."
                })

        newBid = request.POST['bid']
        if newBid is None:
            newBid = 0.00

        count = Bid.objects.filter(prodid=id, bid=newBid).count()
        if count is None:
            count = 0

        if count == 0:
            # Check to make sure the bid is larger than the starting bid or any existing bid(s)
            price = Listing.objects.values_list('price', flat=True).get(pk=id)
            currentBid = Bid.objects.filter(prodid=id).aggregate(Max('bid'))['bid__max']
    
            if currentBid is None:
                currentBid = 0.0
            
            if float(newBid) > float(price) and float(newBid) > float(currentBid):
                bid = Bid(title=title, prodid=id, bid=float(newBid), userstamp=bidder)
                bid.save()

                return render(request, "auctions/listing.html", {
                    "listing": Listing.objects.get(pk=id),
                    "currentBid": newBid,
                    "currentBidder": bidder,
                    "numBids": Bid.objects.filter(title=title).count(),
                    "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count(),
                    "message": "Bid successfully submitted."
                })
            else:
                if int(price) > int(currentBid):
                    newBid = price
                else:
                    newBid = currentBid
                return render(request, "auctions/listing.html", {
                    "listing": Listing.objects.get(pk=id),
                    "currentBid": newBid,
                    "currentBidder": bidder,
                    "numBids": Bid.objects.filter(title=title).count(),
                    "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count(),
                    "message": "Error: New bid must greater than the current bid."
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(pk=id),
                "currentBid": newBid,
                "currentBidder": bidder,
                "numBids": Bid.objects.filter(title=title).count(),
                "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count(),
                "message": "Error: New bid must greater than the current bid."
            })
    else:
        return render(request, "auctions/listing.html")
        

def category(request):
    return render(request, "auctions/category.html", {
        "categories": Listing.objects.values('category').distinct(),
        "watchlistCount": Watchlist.objects.filter(userstamp=request.user).count()
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

