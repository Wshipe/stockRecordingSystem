from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('', views.transactions, name="transactions"),
    path('preferences/', views.notification_preferences, name='notification_preferences'),
    path('notifications/', views.view_notifications, name='notifications'),
    path('search/', views.search, name='search'),
    path('export_to_pdf/', views.export_to_pdf, name='export_to_pdf'),
    path('watchlist/create/', views.create_watchlist, name='create_watchlist'),
    path('watchlists/', views.watchlist_list, name='watchlist_list'),
    path('watchlist/<int:pk>/', views.watchlist_detail, name='watchlist_detail'),
    path('watchlist/<int:pk>/delete/', views.delete_watchlist, name='delete_watchlist'),
    path('watchlist/<int:watchlist_id>/add_stock/', views.add_stock_to_watchlist, name='add_stock_to_watchlist'),
    path('watchlist/<int:watchlist_id>/delete_stock/<int:stock_id>/', views.delete_stock_from_watchlist, name='delete_stock_from_watchlist'),
    path('', views.homepage, name='home-page'),
    path('register/', views.register, name='register'),
    path('my-login/', views.my_login, name='my-login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/', views.transactions, name='transactions'),
    path('user-logout/', views.user_logout, name='user-logout'),
    path('notes/', views.notes, name='notes'),
    path('capitalgains/', views.capitalgains, name='capitalgains'),
    path('notes/create/', views.create_note, name='create-note'),
    path('notes/edit/<int:note_id>/', views.edit_note, name='edit-note'),
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete-note'),
    path('add-stock/', views.add_stock, name='add_stock'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
]