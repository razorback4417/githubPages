from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import json

from django.core.paginator import Paginator

from .models import User, Post, Like, Follower


def index(request):
    if request.method == "POST":
        userstamp = request.POST["userStamp"]
        content = request.POST["content"]
        newPost = Post(userstamp=userstamp, content=content)
        newPost.save()
        
        posts = Post.objects.all().order_by("-timestamp")
        
        fullpostlist = []
        for post in posts:
            like_dict = count_likes(post.id, request.user)
            fullpostlist.append({
                "id": post.id,
                "userstamp": post.userstamp,
                "content": post.content,
                "timestamp": post.timestamp,
                "like": like_dict['num_like'],
                "user_like": like_dict['user_like']
            })
        
        paginator = Paginator(fullpostlist, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "pageTitle": "All Posts",
            "posts": page_obj,
        })
    
    else:
        posts = Post.objects.all().order_by("-timestamp")
        
        fullpostlist = []
        for post in posts:
            like_dict =count_likes(post.id, request.user)
            fullpostlist.append({
                "id": post.id,
                "userstamp": post.userstamp,
                "content": post.content,
                "timestamp": post.timestamp,
                "like": like_dict['num_like'],
                "user_like": like_dict['user_like']
            })
        
        paginator = Paginator(fullpostlist, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, "network/index.html", {
            "pageTitle": "All Posts",
            "posts": page_obj,
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


def count_likes(postID, current_user):
    like_dict = {
        'num_like': 0,
        'user_like': 'Like'
    }

    try:
        like_dict['num_like'] = Like.objects.filter(postID=postID).count()
        try:
            Like.objects.get(postID=postID, userstamp=current_user)
            like_dict['user_like'] = 'Unlike'
        except ObjectDoesNotExist:
            pass
    except ObjectDoesNotExist:
        pass
    return like_dict
                     
@csrf_exempt
@login_required
def toggle_like(request):
    data = json.loads(request.body)
    print("data is ", data['postID'])
    like_count = Like.objects.filter(userstamp=data['cur_username'], postID=data['postID']).count()
    print("reach one")
    if like_count > 0:
        like_entry = Like.objects.get(userstamp=data['cur_username'], postID=data['postID'])
        like_entry.delete()
    else:
        print("reach two")
        like_entry = Like(userstamp=data['cur_username'], postID=data['postID'])
        like_entry.save()
        print("reach three")
    return HttpResponse(status=204)


def save_post(request):
    data = json.loads(request.body)
    Post.objects.filter(pk=data['postID']).update(content=data['newContent'])
    return HttpResponse(status=204)

def following(request):
    
    author_list = Follower.objects.filter(follower=request.user).values_list('author', flat=True)
    print("author_list", author_list)
    
    posts = Post.objects.filter(id=0)
    
    if author_list:
        for author in author_list:
            posts |= (Post.objects.filter(userstamp=author)) #|= is posts.union

    print("posts is", posts)

    fullpostlist = []
    for post in posts:
        like_dict = count_likes(post.id, request.user)
        fullpostlist.append({
            "id": post.id,
            "userstamp": post.userstamp,
            "content": post.content,
            "timestamp": post.timestamp,
            "like": like_dict['num_like'],
            "user_like": like_dict['user_like']
        })

    paginator = Paginator(fullpostlist, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "pageTitle": "Following",
        "posts": page_obj,
    })

def profile(request, userProfile):
    
    if request.method == 'GET':
        numFollowers = Follower.objects.filter(author=userProfile).count()
        
        numFollowing = Follower.objects.filter(follower=userProfile).count()
        
        currentFollower = Follower.objects.filter(author=userProfile, follower=request.user).count()
        
        if currentFollower == None:
            currentFollower = 0
        
        posts = Post.objects.all().order_by("-timestamp")
        fullpostlist = []
        for post in posts:
            like_dict =count_likes(post.id, request.user)
            if (userProfile == post.userstamp):
                fullpostlist.append({
                    "id": post.id,
                    "userstamp": post.userstamp,
                    "content": post.content,
                    "timestamp": post.timestamp,
                    "like": like_dict['num_like'],
                    "user_like": like_dict['user_like']
                })
        paginator = Paginator(fullpostlist, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/profile.html", {
            "pageTitle": "Profile",
            "userProfile": userProfile,
            "followers": numFollowers,
            "following": numFollowing,
            "posts": page_obj,
            "currentFollower": currentFollower
        })

    elif request.method == 'POST':
        followerCount = Follower.objects.filter(author=userProfile, follower=request.user).count()

        if followerCount == None:
            followerCount = 0

        if followerCount > 0:
            follower = Follower.objects.get(author=userProfile, follower=request.user)
            follower.delete()
            currentFollower = 0
        else:
            newFollower = Follower(author=userProfile, follower=request.user)
            newFollower.save()
            print("FOLLOWED NEW USER FOLLOWED NEW USER")
            currentFollower = 1

        numFollowers = Follower.objects.filter(author=userProfile).count()

        numFollowing = Follower.objects.filter(follower=userProfile).count()

        posts = Post.objects.all().order_by("-timestamp")
        fullpostlist = []
        for post in posts:
            like_dict =count_likes(post.id, request.user)
            if (userProfile == post.userstamp):
                fullpostlist.append({
                    "id": post.id,
                    "userstamp": post.userstamp,
                    "content": post.content,
                    "timestamp": post.timestamp,
                    "like": like_dict['num_like'],
                    "user_like": like_dict['user_like']
                })
        paginator = Paginator(fullpostlist, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/profile.html", {
            "pageTitle": "Profile",
            "userProfile": userProfile,
            "followers": numFollowers,
            "following": numFollowing,
            "posts": page_obj,
            "currentFollower": currentFollower
        })
