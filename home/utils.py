import random
from .models import Email_Verification_Code
from django.core.mail import send_mail


# Send_Verification_Code_On_Email
def send_verification_code(user):
    code = f"{random.randint(0, 999999):06d}"
    Email_Verification_Code.objects.create(user=user, code=code)

    send_mail(
        subject="Email_Verification_Code",
        message=f"Your verification code is {code}",
        from_email="Booksyard",
        recipient_list=[user.email],
        fail_silently=False,
    )