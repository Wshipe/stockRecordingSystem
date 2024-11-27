from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='home_page'),
    path('register/', views.register, name='register'),
    path('my-login/', views.my_login, name='my-login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('transactions/', views.transactions, name='transactions'),
    path('user-logout/', views.user_logout, name='user-logout'),
    path('notes/', views.notes, name='notes'),
    path('capitalgains/', views.capitalgains, name='capitalgains'),
]