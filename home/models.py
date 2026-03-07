import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    

# Cart Data_Base
class Cart_Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.book_name} x{self.quantity}"
    
    @property
    def total_price(self):
        return round(self.book.price * self.quantity, 2)
    

# Email_Verification
class Email_Verification_Code(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=15)
    
    def __str__(self):
        return f"{self.user.username} - {self.code}"
    

# Profile Data_Base 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default_profile_avatar.jpg")

    def __str__(self):
        return self.user.username
    

# Comment Data_Base
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.book_name[:15]}"