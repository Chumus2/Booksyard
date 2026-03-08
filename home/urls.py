from django.contrib.auth import views as auth_views
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

    path("book/<int:book_id>/", views.book_detail, name="book_detail"),
    path("book/<int:book_id>/comment/", views.create_comment, name="create_comment"),
    path("comment/delete/<int:comment_id>/", views.delete_comment, name="delete_comment"),
    path("comment/edit/<int:comment_id>/", views.edit_comment, name="edit_comment"),

    path("account/", views.account, name="account"),
    path("account/delete/", views.delete_account, name="delete_account"),
    path("account/change_username/", views.change_name, name="change_username"),
    path("account/change_email/", views.change_email, name="change_email"),
    path("account/change_avatar/", views.change_avatar, name="change_avatar"),
    path("cart/add/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path("account/change_country/", views.change_country, name="change_country"),
    path("account/enable_authentication/", views.enable_authentication, name="enable_authentication"),

    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="home/password_reset.html"
    ), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(
        template_name="home/password_reset_done.html"
    ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="home/password_reset_confirm.html"
    ), name="password_reset_confirm"),
    path("reset_done/",  auth_views.PasswordResetCompleteView.as_view(
        template_name="home/password_reset_complete.html"
    ), name="password_reset_complete"),

    path("cart/", views.cart_view, name="cart"),
    path("cart/cleared/", views.clear_cart, name="clear_cart"),
    path("cart/remove/<int:item_id>/", views.remove_item_from_cart, name="remove_item")
]