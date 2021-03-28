from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from .models import *
import json
import requests
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import environ
from django.core.paginator import Paginator


# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


# Create your views here.
@login_required
def index(request):
    country = request.GET.get("country")
    if country == None:
        country = "us"

    category = request.GET.get("category")
    if category == None:
        category = "general"

    try:
        result_page = int(request.GET.get("page"))
    except:
        result_page = 1
    
    if request.method == "POST":
        try:
            country = request.POST["country"]
            category = request.POST["category"]
        except:
            #in case user does not choose country and/or category
            return HttpResponseRedirect(reverse("index"))

    news_request = requests.get(f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&pageSize=100&apiKey={env('API_KEY')}")   
    news = json.loads(news_request.content)

    total_results = int(news["totalResults"])

    news = Paginator(news["articles"], 20)
    page = news.page(result_page)

    return render(request, "news/index.html", {"view":"index", "country":country, "category":category, "news":page, "page":result_page, "has_next":page.has_next()})


@login_required
def search_keyword(request):
    if request.method == "POST":
        keyword = request.POST["keyword"]
        result_page = 1
    else:
        #GET request - retrieve keyword and result_page
        keyword = request.GET.get("keyword")
        result_page = int(request.GET.get("page"))

    news_request = requests.get(f"https://newsapi.org/v2/everything?q={keyword}&from={datetime.today().strftime('%Y-%m-%d')}&sortBy=popularity&page={result_page}&apiKey={env('API_KEY')}")   
    news = json.loads(news_request.content)

    total_results = int(news["totalResults"])

    if 20*result_page < total_results  and 20*result_page < 100:
        has_next = True
    else:
        has_next = False

    return render(request, "news/index.html", {"view":"search", "news":news["articles"], "keyword":keyword, "page":result_page, "has_next":has_next})


@csrf_exempt
def manage_bookmarks(request):
    if (request.method != "POST" and request.method != "PUT"):
        return JsonResponse({"error":"Your request is not POST neither PUT"}, status=404, safe=False)
    
    data = json.loads(request.body.decode("utf-8"))
    
    type_of_action = data["type"]
    
    if type_of_action == "bookmark":
        bookmark = Bookmark(user=request.user, title=data['title'], card_description=data['card_description'], image_url=data['image_url'],
        article_url=data['url'])
        bookmark.save()
        return JsonResponse({"message": "Article bookmarked successfuly"}, status=201)

    #unbookmark article
    bookmark = Bookmark.objects.get(user=request.user, article_url=data['url'])
    bookmark.delete()
    return JsonResponse({"bookmark": "deleted"}, status=201)


@login_required
def show_bookmarks(request):
    try:
        result_page = int(request.GET.get("page"))
    except:
        result_page = 1

    bookmarks = list(reversed(Bookmark.objects.filter(user=request.user)))
    bookmarks = {"articles": [bookmark.serialize() for bookmark in bookmarks]}

    bookmarks = Paginator(bookmarks["articles"], 20)
    page = bookmarks.page(result_page)

    return render(request, "news/index.html", {"view":"bookmark", "news":page, "page":result_page, "has_next":page.has_next()})


@login_required
def get_user_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    bookmarks = [bookmark.article_url for bookmark in bookmarks]
    return JsonResponse({"article_urls": bookmarks}, status=201)

       
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