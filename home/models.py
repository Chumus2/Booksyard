from django.db import models
from multiselectfield import MultiSelectField


TYPES_LIST = [
    ("paperbook", "Paperbook"),
    ("e_book", "E-Book"),
    ("audiobook", "Audiobook"),
]

GENRES_LIST = [
    ("fantasy", "Fantasy"), ("dark_fantasy", "Dark_Fantasy"), ("action", "Action"),
    ("adventure", "Adventure"), ("shonen", "Shonen"), ("horror", "Horror"),
    ("sci_fi", "Sci_Fi"), ("mystery", "Mystery"), ("thriller", "Thriller"),
    ("romance", "Romance"), ("historical", "Historical"), ("drama", "Drama"),
    ("adventure", "Adventure"), ("comedy", "Comedy"), ("poetry", "Poetry"),
    ("biography", "Biography"), ("manga", "Manga"),
]


# Book Data_Base
class Book(models.Model):
    book_name = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    type = models.CharField(max_length=30, choices=TYPES_LIST)
    genre = MultiSelectField(choices=GENRES_LIST, blank=True)
    description = models.TextField()
    price = models.FloatField()
    date = models.DateField()
    cover = models.ImageField(upload_to="book_cover/", blank=True, null=True)

    def __str__(self):
        return self.book_name