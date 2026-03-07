from django.contrib import admin
from .models import *


# Register Book Data_Base
admin.site.register(Book)

# Register Genre Data_Base
admin.site.register(Genre)

# Register Cart_Item Data_Base
admin.site.register(Cart_Item)

# Register Email_Verification_Code Data_Base
admin.site.register(Email_Verification_Code)

# Register Profile Data_Base
admin.site.register(Profile)

# Register Comment Data_Base
admin.site.register(Comment)