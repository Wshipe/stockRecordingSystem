from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import views
from .models import NotificationPreference
from celery import shared_task
from .models import Notification
from .models import Stock, Transaction
from io import BytesIO
from reportlab.pdfgen import canvas

# Create your views here.
# comment

def home(request):
    return render(request, 'webstock/home.html')

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