from django.urls import path
from . import views


urlpatterns = [
    path("", views.book_list, name="home"),
    path("page-<int:page>/", views.book_list, name="home_paginated"),
    path("sorted/page-<int:page>/", views.book_list, name="sorted_books"),

    path("log_in/", views.log_in, name="login"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("verify/", views.verify_code, name="verify_code"),
    path("logout/", views.log_out, name="log_out"),

    path("account/", views.account, name="account"),
    path("account/change_username/", views.change_name, name="change_username"),
    path("account/change_email/", views.change_email, name="change_email"),
    path("book/<str:book_id>/", views.book_detail, name="book_detail"),
    path("cart/add/<int:book_id>/", views.add_to_cart, name="add_to_cart"),

    path("cart/", views.cart_view, name="cart"),
    path("cart/cleared/", views.clear_cart, name="clear_cart"),
    path("cart/remove/<int:item_id>/", views.remove_item_from_cart, name="remove_item")
]