from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from .models import *
import json
import requests


# Create your views here.
def index(request):
    #default values us and general 
    country = 'us'
    category = 'general'

    if request.method == "POST":
        try:
            country = request.POST['country']
            category = request.POST['category']
        except:
            #in case user does not choose country and/or category
            return HttpResponseRedirect(reverse("index"))

    news_request = requests.get(f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey=ee4879eace1c436faf001ee8b69971c8")   
    news = json.loads(news_request.content)
    return render(request, "news/index.html", {"news":news})


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
            return render(request, "news/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "news/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "news/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "news/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "news/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))