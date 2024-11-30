from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    user_ID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    security_question = models.CharField(max_length=50)




class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else f"Note {self.id}"
    
class Watchlist(models.Model):
    Watchlist_ID = models.AutoField(primary_key=True)
    Watchlist_name = models.CharField(max_length= 32)
    Market_Symbol = models.CharField(max_length=10)
    Current_Symbol_price = models.FloatField()
    

class TradHistory(models.Model):
    #Market symbol from watch list * Unsure of field type
    Watchlist_ID = models.ForeignKey(Watchlist)
    
    #Date Stock was bought * copied field from notes table unsure of logic
    Date_Bought = models.DateTimeField(auto_now_add = True)

    #Date stock was sold * same as Date_Bought
    Date_Sold = models.DateTimeField(auto_now_add = True)