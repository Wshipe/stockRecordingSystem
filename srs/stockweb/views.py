from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import views
from .models import NotificationPreference
from celery import shared_task
from .models import Notification
from .models import Stock, Transaction
from io import BytesIO
from reportlab.pdfgen import canvas
from weasyprint import HTML
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, NoteForm, AddStockForm
from django.contrib.auth.decorators import login_required
from .forms import NoteForm
from .models import Note
from django.shortcuts import get_object_or_404
from .forms import WatchListForm
from .models import WatchList
from .models import Stock, WatchListStock
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def homepage(request):
    return render(request, 'stockweb/index.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my-login')

    context = {'registerform': form}

    return render(request, 'stockweb/register.html', context=context)
def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')

    context = {'loginform': form}
    return render(request, 'stockweb/my-login.html', context=context)

@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'stockweb/dashboard.html')

def transactions(request):
    return render(request, 'stockweb/transactions.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def notes(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'stockweb/notes.html', {'notes': notes})

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            # Create but don't save the new note instance
            new_note = form.save(commit=False)
            # Assign the current user to the note
            new_note.user = request.user
            # Save the note to the database
            new_note.save()
            return redirect('notes')
    else:
        form = NoteForm()
    return render(request, 'stockweb/create-note.html', {'form': form})

def capitalgains(request):
    return render(request, 'stockweb/capitalgains.html')

@login_required
def edit_note(request, note_id):
    """View to edit an existing note."""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes')
    else:
        form = NoteForm(instance=note)
    return render(request, 'stockweb/edit-note.html', {'form': form, 'note': note})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('notes')
    return render(request, 'stockweb/delete-note.html', {'note': note})



#event notification
@login_required
def notification_preferences(request):
    if request.method == "POST":
        email = request.POST.get('email_notifications') == 'on'
        sms = request.POST.get('sms_notifications') == 'on'
        in_app = request.POST.get('in_app_notifications') == 'on'
        preferences, _ = NotificationPreference.objects.get_or_create(user=request.user)
        preferences.email_notifications = email
        preferences.sms_notifications = sms
        preferences.in_app_notifications = in_app
        preferences.save()
        return redirect('preferences')
    preferences, _ = NotificationPreference.objects.get_or_create(user=request.user)
    return render(request, 'stockweb/preferences.html', {'preferences': preferences})

@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'stockweb/notifications.html', {'notifications': notifications})

@shared_task
def check_notifications():
    notifications = Notification.objects.filter(status='Pending')
    #for notification in notifications:
        # Logic to check stock condition
        #if condition_met(notification.stock, notification.condition):
        #    send_notification(notification.user, notification)
        #    notification.status = 'Sent'
        #    notification.save()

#search
@login_required
def search(request):
    query = request.GET.get('query')
    filter_type = request.GET.get('filter_type')  # e.g., 'sector' or 'date'
    results = []

    if filter_type == 'sector':
        results = Stock.objects.filter(sector=query)  # Assuming a 'sector' field in Stock
    elif filter_type == 'date':
        results = Transaction.objects.filter(date=query)
    elif filter_type == 'ticker':
        results = Stock.objects.filter(ticker=query)

    return render(request, 'stockweb/search.html', {'results': results})

def export_to_pdf(request):
    query = request.GET.get('query')
    results = Transaction.objects.filter(stock__ticker=query)
    html = render_to_string('transactions_pdf.html', {'results': results})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{query}_transactions.pdf"'
    HTML(string=html).write_pdf(response)
    return response


# watchlist

def create_watchlist(request):
    if request.method == "POST":
        form = WatchListForm(request.POST)
        if form.is_valid():
            watchlist = form.save(commit=False)
            watchlist.user = request.user
            watchlist.save()
            messages.success(request, "Watchlist created successfully!")
            return redirect('watchlist_list')
        else:
            messages.error(request, "Failed to create watchlist. Please try again.")
    else:
        form = WatchListForm()
    return render(request, 'stockweb/create_watchlist.html', {'form': form})


def add_stock_to_watchlist(request, stock_id):
    stock = Stock.objects.get(id=stock_id)
    if request.method == "POST":
        form = AddStockForm(request.user, request.POST)
        if form.is_valid():
            watchlist = form.cleaned_data['watchlist_id']
            WatchListStock.objects.create(watchlist=watchlist, stock=stock)
            return redirect('watchlist_detail', pk=watchlist.id)
    else:
        form = AddStockForm(request.user)
    return render(request, 'stockweb/add_stock.html', {'form': form, 'stock': stock})


def delete_stock_from_watchlist(request, stock_id, watchlist_id):
    WatchListStock.objects.filter(watchlist_id=watchlist_id, stock_id=stock_id).delete()
    return redirect('watchlist_detail', pk=watchlist_id)


def delete_watchlist(request, pk):
    WatchList.objects.filter(id=pk, user=request.user).delete()
    return redirect('watchlist_list')

def watchlist_detail(request, pk):
    watchlist = get_object_or_404(WatchList, pk=pk, user=request.user)
    return render(request, 'stockweb/watchlist_detail.html', {'watchlist': watchlist})

def watchlist_list(request):
    watchlists = WatchList.objects.filter(user=request.user)
    return render(request, 'stockweb/watchlist_list.html', {'watchlists': watchlists})






#commentt