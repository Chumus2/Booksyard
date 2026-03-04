from django.core.paginator import Paginator
from django.shortcuts import render
from django.db import models
from .models import Book, Genre


def book_list(request, page=1):
    books = Book.objects.all()
    genres = Genre.objects.all()
    languages = Book.objects.values_list("language", flat=True).distinct()

    # Search
    book_search = request.GET.get("book_search", "").strip()
    if book_search:
        books = books.filter(
            models.Q(book_name__icontains=book_search) |
            models.Q(author__icontains=book_search)
        )

    # Genres filtration
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

    total_books = books.count()
    paginator = Paginator(books, 28)
    page_obj = paginator.get_page(page)

    context = {
        "page_obj": page_obj,
        "genres": genres,
        "selected_genres": list(map(int, selected_genres)),
        "current_sort": sort_option,
        "languages": languages,
        "selected_languages": selected_languages,
        "total_books": total_books,
        "book_search": book_search
    }

    return render(request, "home/home.html", context)