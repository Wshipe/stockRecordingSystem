from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('', views.watchlist, name="watchlist"),
    path('', views.transactions, name="transactions"),
]