import re
from .utils import send_verification_code
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Book, Genre, Cart_Item, Email_Verification_Code
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



# Book_List
def book_list(request, page=1):
    books = Book.objects.all()
    genres = Genre.objects.all()
    languages = Book.objects.values_list("language", flat=True).distinct()
    types = Book.objects.values_list("type", flat=True).distinct()

    # Cart_Items
    if request.user.is_authenticated:
        cart_items = Cart_Item.objects.filter(user=request.user)
        total_cart_items = cart_items.count()
    else:
        total_cart_items = 0

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
        "total_cart_items": total_cart_items,
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
            request.session["verify_user"] = user.id
            send_verification_code(user)

            return redirect("verify_code")
        else:
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
        elif not re.search(r"[A-Z]", password):
            return render(request, "home/sign_up.html", {"error": "Password must contain at least one uppercase letter."})
        elif not re.search(r"[a-z]", password):
            return render(request, "home/sign_up.html", {"error": "Password must contain at least one lowercase letter."})
        elif not re.search(r"\d", password):
            return render(request, "home/sign_up.html", {"error": "Password must contain at least one digit."})
        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return render(request, "home/sign_up.html", {"error": "Password must contain at least one special character (!@#$%^&* etc.)."})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)

        return redirect("home")

    return render(request, "home/sign_up.html")


# Verify_Code
def verify_code(request):
    user_id = request.session.get("verify_user")

    if not user_id:
        return redirect("login")
    
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        code = request.POST.get("code")
        verification = Email_Verification_Code.objects.filter(
            user=user, code=code
        ).order_by("-created_at").first()

        if verification and not verification.is_expired():
            login(request, user)
            del request.session["verify_user"]

            return redirect("home")
        
    return render(request, "home/verify_code.html")


# Log_Out
def log_out(request):
    logout(request)
    return redirect("login")


# Account
@login_required(login_url="login")
def account(request):
    user_obj = request.user
    cart_items = Cart_Item.objects.filter(user=user_obj)
    total_cart_items = cart_items.count()

    message = request.session.pop("message", None)
    message2 = request.session.pop("message2", None)

    context = {
        "user_obj": user_obj,
        "total_cart_items": total_cart_items,
        "message": message,
        "message2": message2
    }
    
    return render(request, "home/account.html", context)


# Change_Name
@login_required(login_url="login")
def change_name(request):
    if request.method == "POST":
        new_username = request.POST.get("new_username", "").strip()

        if not new_username:
            request.session["message"] = "Username cannot be empty."
        elif User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
            request.session["message"] = "This username is already taken."
        else:
            request.user.username = new_username
            request.user.save()
            request.session["message"] = "Username updated successfully!"

    return redirect("account")


# Change_Email
@login_required(login_url="login")
def change_email(request):
    if request.method == "POST":
        new_email = request.POST.get("new_email", "").strip()

        if not new_email:
            request.session["message2"] = "Email cannot be empty."
        elif User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
            request.session["message2"] = "This email is already registered."
        else:
            request.user.email = new_email
            request.user.save()
            request.session["message2"] = "Email updated successfully."

    return redirect("account")


# Change_Avatar 
@login_required(login_url="login")
def change_avatar(request):
    if request.method == "POST":
        avatar = request.FILES.get("avatar")

        if avatar:
            profile = request.user.profile
            profile.avatar = avatar
            profile.save()

    return redirect("account")


# Delete_Account
@login_required(login_url="login")
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()

        return redirect("home")
    
    return redirect("account")


# Book_Detail
def book_detail(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)

    return render(request, "home/book.html", {"book_obj": book_obj})


# Add_To_Cart
@login_required(login_url="login")
def add_to_cart(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    amount = int(request.POST.get("quantity", 1))
    cart_item, created = Cart_Item.objects.get_or_create(user=request.user, book=book_obj)

    if created:
        cart_item.quantity = amount
    else:
        cart_item.quantity += amount
    cart_item.save()

    return redirect("home")


# Cart_View
@login_required(login_url="login")
def cart_view(request):
    cart_items = Cart_Item.objects.filter(user=request.user)
    total_cart_items = cart_items.count()
    total = sum(item.total_price for item in cart_items)

    context = {
        "cart_items":cart_items,
        "total": round(total, 2),
        "total_cart_items": total_cart_items
    }

    return render(request, "home/cart.html", context)


# Cart_Clear_All
@login_required(login_url="login")
def clear_cart(request):
    if request.method == "POST":
        Cart_Item.objects.filter(user=request.user).delete()

    return redirect("cart")


# Remove_Item_From_Cart
@login_required(login_url="login")
def remove_item_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart_Item, id=item_id, user=request.user)
    
    if request.method == "POST":
        cart_item.delete()

    return redirect("cart")