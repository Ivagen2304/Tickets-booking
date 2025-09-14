from django import forms
from .models import Station
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PaymentForm(forms.Form):
    amount = forms.DecimalField( 
        max_digits=10, 
        decimal_places=2,
        label="Сума"
    )

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class SearchForm(forms.Form):
    origin = forms.ModelChoiceField(queryset=Station.objects.all(), label="Звідки")
    destination = forms.ModelChoiceField(queryset=Station.objects.all(), label="Куди")
    date = forms.DateField(label="Дата", widget=forms.DateInput(attrs={"type":"date"}))

class BookingForm(forms.Form):
    passenger_name = forms.CharField(label="ПІБ пасажира", max_length=120)
