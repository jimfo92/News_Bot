from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("search_keyword", views.search_keyword, name="search_keyword"),
    path("manage_bookmark", views.manage_bookmarks, name="manage_bookmarks"),
    path("show_bookmarks", views.show_bookmarks, name="show_bookmarks")
]