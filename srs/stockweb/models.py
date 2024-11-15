from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomerUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    security_question = models.CharField(max_length=50)

