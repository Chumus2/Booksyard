from django.db import models


TYPES_LIST = [
    ("paperbook", "Paperbook"),
    ("e_book", "E-Book"),
    ("audiobook", "Audiobook"),
]


# Genre Data_Base
class Genre(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Book Data_Base
class Book(models.Model):
    book_name = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    type = models.CharField(max_length=30, choices=TYPES_LIST)
    genre = models.ManyToManyField(Genre, related_name="books")
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    date = models.DateField(blank=True, null=True)
    cover = models.ImageField(upload_to="book_cover/", blank=True, null=True)

    def __str__(self):
        return self.book_name