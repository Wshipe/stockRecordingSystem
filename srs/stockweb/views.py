from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import views
from . forms import CreateUserForm

# Create your views here.
# comment

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


    return render(request, 'stockweb/register.html', context)

def my_login(request):
    return render(request, 'stockweb/my-login.html')

def dashboard(request):
    return render(request, 'stockweb/dashboard.html')

def transactions(request):
    return render(request, 'stockweb/transactions.html')

def watchlist(request):
    return render(request, 'stockweb/watchlist.html')


