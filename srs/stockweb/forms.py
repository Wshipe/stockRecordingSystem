from .models import Note
from .models import WatchList
from .models import WatchListStock
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import TextInput, PasswordInput
from .models import Note, WatchList, WatchListStock, Stock, Transaction


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter note title (optional)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your note here...',
                'rows': 5
            }),
        }


class WatchListForm(forms.ModelForm):
    class Meta:
        model = WatchList
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter watch list name'}),
        }

class AddStockToWatchListForm(forms.Form):
    stock = forms.ModelChoiceField(
        queryset=None,  # Will be set dynamically
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Select Stock"
    )

    def __init__(self, user, watchlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.exclude(
            id__in=watchlist.stocks.values_list('stock_id', flat=True)
        )


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['ticker', 'company_name', 'current_price']
        widgets = {
            'ticker': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock ticker'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}),
            'current_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter current price'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['stock', 'transaction_type', 'shares', 'price', 'date']
        widgets = {
            'stock': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'shares': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of shares'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter transaction price'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }