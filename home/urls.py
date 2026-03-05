from django.urls import path
from . import views


urlpatterns = [
    path("", views.book_list, name="home"),
    path("page-<int:page>/", views.book_list, name="home_paginated"),
    path("sorted/page-<int:page>/", views.book_list, name="sorted_books"),
    path("log_in/", views.log_in, name="login"),
    path("sign_up/", views.sign_up, name="sign_up")
]