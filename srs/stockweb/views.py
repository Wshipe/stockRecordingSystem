from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import views
from .models import NotificationPreference
from celery import shared_task
from .models import Notification
from .models import Stock, Transaction
from io import BytesIO
from reportlab.pdfgen import canvas
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, NoteForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import NoteForm
from .models import Note
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

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

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')

    context = {'loginform': form}

    return render(request, 'stockweb/my-login.html', context=context)

@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'stockweb/dashboard.html')

def transactions(request):
    return render(request, 'stockweb/transactions.html')

def watchlist(request):
    return render(request, 'stockweb/watchlist.html')

def user_logout(request):
    auth.logout(request)
    return redirect('/')

def notes(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'stockweb/notes.html',{'notes': notes})

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
    return render(request, 'preferences.html', {'preferences': preferences})

def view_notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notifications.html', {'notifications': notifications})


@shared_task
def check_notifications():
    notifications = Notification.objects.filter(status='Pending')
    for notification in notifications:
        # Logic to check stock condition
        if condition_met(notification.stock, notification.condition):
            send_notification(notification.user, notification)
            notification.status = 'Sent'
            notification.save()

#search
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

    return render(request, 'search.html', {'results': results})


def export_to_pdf(request):
    query = request.GET.get('query')
    results = Transaction.objects.filter(stock__ticker=query)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{query}_transactions.pdf"'
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 800, f"Transactions for {query}")

    y = 750
    for result in results:
        pdf.drawString(100, y,
                       f"Date: {result.date}, Type: {result.transaction_type}, Shares: {result.shares}, Price: ${result.price}")
        y -= 20

    pdf.save()
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()
    return response