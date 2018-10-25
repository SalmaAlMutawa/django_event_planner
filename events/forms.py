from django import forms
from django.contrib.auth.models import User
from .models import Event, Book
from django.contrib.auth.forms import PasswordChangeForm

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['organizer', 'slug', ]

		widgets = {
		'date': forms.DateInput(attrs={'type':'date'}),
		'time':forms.TimeInput(attrs={'type':'time'}),
		}

class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['tickets',]


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]


class CancelBookForm(forms.Form):
		num_cancelled_tickets=forms.IntegerField(min_value = 0)