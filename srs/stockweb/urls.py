from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('', views.watchlist, name="watchlist"),
    path('', views.transactions, name="transactions"),
    path('preferences/', views.notification_preferences, name='preferences'),
    path('notifications/', views.view_notifications, name='notifications'),
    path('search/', views.search, name='search'),
    path('export_to_pdf/', views.export_to_pdf, name='export_to_pdf'),
]