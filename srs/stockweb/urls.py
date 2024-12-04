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
    path('watchlist/', views.create_watchlist, name='create_watchlist'),
    path('watchlist/<int:pk>/', views.watchlist_detail, name='watchlist_detail'),
    path('watchlist/<int:pk>/delete/', views.delete_watchlist, name='delete_watchlist'),
    path('watchlist/add_stock/<int:stock_id>/', views.add_stock_to_watchlist, name='add_stock'),
    path('watchlist/<int:watchlist_id>/delete_stock/<int:stock_id>/', views.delete_stock_from_watchlist, name='delete_stock_from_watchlist'),
]
# comment