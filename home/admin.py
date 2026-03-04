from django.contrib import admin
from .models import Book, Genre


# Register Book Data_Base
admin.site.register(Book)

# Register Genre Data_Base
admin.site.register(Genre)