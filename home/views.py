from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book


def book_list(request, page=1):
    books = Book.objects.all()
    paginator = Paginator(books, 28)
    page_obj = paginator.get_page(page)

    context = {
        "page_obj": page_obj
    }

    return render(request, "home/home.html", context)


def sorted_books(request, page=1):
    books = Book.objects.all()
    sort_option = request.GET.get("sort")
    selected_genres = request.GET.getlist("genre")

    allowed_sorts = [
        "book_name", "-book_name",
        "price", "-price",
        "date", "-date"
    ]

    if sort_option in allowed_sorts:
        books = books.order_by(sort_option)

    paginator = Paginator(books, 28)
    page_obj = paginator.get_page(page)
    context = {
        "page_obj": page_obj,
        "current_sort": sort_option,
        "current_genres": selected_genres,
    }

    return render(request, "home/home.html", context)