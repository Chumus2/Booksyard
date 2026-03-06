import re
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Book, Genre
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Book_List
def book_list(request, page=1):
    books = Book.objects.all()
    genres = Genre.objects.all()
    languages = Book.objects.values_list("language", flat=True).distinct()
    types = Book.objects.values_list("type", flat=True).distinct()

    # Search
    book_search = request.GET.get("book_search", "").strip()
    if book_search:
        books = books.filter(
            models.Q(book_name__icontains=book_search) |
            models.Q(author__icontains=book_search)
        )

    # Genres
    selected_genres = request.GET.getlist("genres")
    if selected_genres:
        books = books.filter(genre__id__in=selected_genres).distinct()

    # Sort
    sort_option = request.GET.get("sort")
    allowed_sorts = ["book_name", "-book_name", "price", "-price", "date", "-date"]
    if sort_option in allowed_sorts:
        books = books.order_by(sort_option)

    # Languages
    selected_languages = request.GET.getlist("language")
    if selected_languages:
        books = books.filter(language__in=selected_languages)

    # Types
    selected_types = request.GET.getlist("type")
    if selected_types:
        books = books.filter(type__in=selected_types)

    total_books = books.count()
    paginator = Paginator(books, 28)
    page_obj = paginator.get_page(page)

    context = {
        "page_obj": page_obj,
        "genres": genres,
        "languages": languages,
        "types": types,
        "current_sort": sort_option,
        "total_books": total_books,
        "book_search": book_search,
        "selected_genres": list(map(int, selected_genres)),
        "selected_languages": selected_languages,
        "selected_types": selected_types
    }

    return render(request, "home/home.html", context)


# Login
def log_in(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "home/login.html", {"error": "Invalid email or password"})

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "home/login.html", {"error": "Incorrect email or password"})

    return render(request, "home/login.html")


# Sign_Up
def sign_up(request):
    
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if not username or not email or not password or not password2:
            return render(request, "home/sign_up.html", {"error": "All fields are required."})

        if password != password2:
            return render(request, "home/sign_up.html", {"error": "Passwords do not match."})
        
        if User.objects.filter(username=username).exists():
            return render(request, "home/sign_up.html", {"error": "Username already taken."})

        if User.objects.filter(email=email).exists():
            return render(request, "home/sign_up.html", {"error": "Email already registered."})
        
        # Password
        if len(password) < 8:
            return render(request, "home/sign_up.html", {"error": "Password must be at least 8 characters."})
        if not re.search(r"[A-Z]", password):
            return render(request, "home/sign_up.html", {"error": "Password must contain at least one uppercase letter."})
        if not re.search(r"[a-z]", password):
            return render(request, "home/sign_up.html", {"error": "Password must contain at least one lowercase letter."})
        if not re.search(r"\d", password):
            return render(request, "home/sign_up.html", {"error": "Password must contain at least one digit."})
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return render(request, "home/sign_up.html", {"error": "Password must contain at least one special character (!@#$%^&* etc.)."})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)

        return redirect("home")

    return render(request, "home/sign_up.html")


# Log_Out
def log_out(request):
    logout(request)
    return redirect("home")


# Account
@login_required(login_url="log_in")
def account(request, username):
    if request.user.username != username:
        return redirect("home")
    
    user_obj = get_object_or_404(User, username=username)

    return render(request, "home/account.html", {"user_obj": user_obj})


# Book_Detail
@login_required(login_url="log_in")
def book_detail(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)

    return render(request, "home/book.html", {"book_obj": book_obj})