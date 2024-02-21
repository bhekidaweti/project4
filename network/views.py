from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json


from .models import User, Post, Follow, Like

def index(request):
    all_posts = Post.objects.all().order_by("id").reverse()

    #Paginator implementation
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_page = paginator.get_page(page_number)

    all_likes = Like.objects.all()
    who_you_liked = []
    try:
        for like in all_likes:
            if like.user.id == request.user.id:
                who_you_liked.append(like.post.id)
    except:
        who_you_liked = []

    return render(request, "network/index.html", {
        "all_posts": all_posts,
        "posts_of_page": posts_of_page,
        "who_you_liked": who_you_liked
    })

def new_post(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))
    
#User profile

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    all_posts = Post.objects.filter(user=user).order_by("id").reverse()

    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(follower=user)

    try:
        check_follow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(check_follow) !=0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False
    
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_of_page = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "all_posts": all_posts,
        "posts_of_page": posts_of_page,
        "username": user.username,
        "following": following,
        "followers": followers,
        "is_following": is_following,
        "user_profile": user

    })
 

def following(request):
    current_user = User.objects.get(pk=request.user.id)
    following_people = Follow.objects.filter(user=current_user)
    all_posts = Post.objects.all().order_by('id').reverse()

    following_posts = []

    for post in all_posts:
        for person in following_people:
            if person.follower == post.user:
                following_posts.append(post)
    #Paginator implementation
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    posts_of_page = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts_of_page": posts_of_page
    })

    return

def follow(request):
    follower = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    user_to_follow = User.objects.get(username=follower)
    f = Follow(user=current_user, follower=user_to_follow)
    f.save()
    user_id = user_to_follow.id    
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def unfollow(request):
    follower = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    user_to_follow = User.objects.get(username=follower)
    f = Follow.objects.get(user=current_user, follower=user_to_follow)
    f.delete()
    user_id = user_to_follow.id    
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))
  
def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Edited successfully", "data": data["content"]})


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
