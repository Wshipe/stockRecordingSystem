from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Stock(models.Model):
    ticker = models.CharField(max_length=10)  # symbols
    company_name = models.CharField(max_length=255)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    gain_loss_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.company_name} ({self.ticker})"


# event notification
class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    in_app_notifications = models.BooleanField(default=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    condition = models.CharField(max_length=255)  # e.g., "Price > $500"
    notified_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Sent', 'Sent')])


# search
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=[('Buy', 'Buy'), ('Sell', 'Sell')])
    shares = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else f"Note {self.id}"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists')
    name = models.CharField(max_length=100)  # e.g., "Tech Stocks"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WatchListStock(models.Model):
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='stocks')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class TradHistory(models.Model):
    # Market symbol from watch list * Unsure of field type
    # Watchlist_ID = models.ForeignKey(Watchlist)

    # Date Stock was bought * copied field from notes table unsure of logic
    Date_Bought = models.DateTimeField(auto_now_add=True)

    # Date stock was sold * same as Date_Bought
    Date_Sold = models.DateTimeField(auto_now_add=True)

# comment