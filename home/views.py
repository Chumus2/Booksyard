from django.shortcuts import render
from .models import Book


def home(request):
    books = Book.objects.all()[:28]
    
    context = {"books": books}

    return render(request, "home/home.html", context)