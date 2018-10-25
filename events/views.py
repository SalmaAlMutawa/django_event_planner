from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, BookForm, UserEditForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Event, Book
import datetime
import requests
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm


def home(request):
    return render(request, 'home_pg.html')

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("events-list")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('events-list')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")


def dashboard (request):
    if request.user.is_anonymous:
        return redirect ('login')
    user = request.user
    today = datetime.datetime.now()
    now = today.time()
    my_events = Event.objects.filter(organizer=user)
    booked_events = Book.objects.filter(user=user, event__date__gte=today)
    attended_events = Book.objects.filter(user=user, event__date__lte=today)

    context = {
        "my_events" : my_events, 
        "booked_events" : booked_events,
        "attended_events": attended_events,
    }
    return render (request, 'dashboard.html', context)

def create_event (request):
    if request.user.is_anonymous:
        return redirect ('login')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit = False)
            event.organizer = request.user
            event.save()
            return redirect ('dashboard')
    context = {
        "form" : form,
    }

    return render (request, 'event-create.html', context)

def event_list (request):
    today = datetime.datetime.now()
    events = Event.objects.filter(date__gte=today.date()).exclude(date=today.date(), time__lt=today.time())
    
    query = request.GET.get('q')
    if query:
        events = events.filter(
            Q (name__icontains = query) |
            Q (description__icontains = query) |
            Q (organizer__username__icontains = query)|
            Q (organizer__first_name__icontains = query)|
            Q (organizer__last_name__icontains = query)
            ).distinct()

    context = {
        "events" : events,
    
    }
    return render (request, 'events_list.html', context)

def event_detail (request, event_slug):
    if request.user.is_anonymous:
        return redirect ('login')

    event = Event.objects.get(slug=event_slug)
    organizer = event.organizer
    bookers = event.book_set.all()
    form = BookForm()

    context = {
        "event" : event,
        "organizer" : organizer,
        "bookers" : bookers,
        "form" : form,
    }
    return render (request, 'event_detail.html', context)


def event_edit (request, event_slug):
    event = Event.objects.get(slug=event_slug)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited!")
            return redirect ('dashboard')
        print (form.errors)
    context = {
        'form' : form,
        'event' : event,
        }
    return render (request, 'edit_event.html', context)

def event_delete(request, event_slug):
    Event.objects.get(slug=event_slug).delete()
    messages.success(request, "Successfully Deleted!")
    return redirect ('dashboard')


def event_book(request, event_slug):
    event = Event.objects.get(slug=event_slug)

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit = False)
            if  (book.tickets <= event.seats_left()):
                book.event = event
                book.user = request.user
                book.save()
                messages.success(request, "Successfully Booked an Event!")
                send_mail(
                    'Event Booked Successfully',
                    ("Welcome to #!\nYou have successfully booked %s ticket(s) for %s.\nIt will be hosted at %s on %s at %s.\n\nWe hope you enjoy the event!\n\nRegards,\nThe # team") %(book.tickets, event.name, event.location, event.date, event.time),
                    'bookeventskw@gmail.com',
                    [book.user.email,],
                    fail_silently = False,
                )

                return redirect ('events-list')
            messages.warning(request, "Not enough available seats, please try again.")           
    return redirect ("event-detail", event_slug=event.slug)

def view_profile (request):
    user = request.user
    context = {
        "user": user,        
    }
    return render (request,'view_profile.html', context)

def edit_profile(request):
    user = request.user
    form = UserEditForm(instance=user)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited your profile!")
            return redirect ('user-profile')
        print (form.errors)
    context = {
        'form' : form,
        'user' : user,
        }
    return render (request, 'edit_profile.html', context)


def change_password(request):
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('edit-profile')
        else:
            messages.warning(request, 'Oops, something went wrong!')
    form = PasswordChangeForm(request.user)

    context={
        "form": form,
    }
    return render(request, 'change_password.html', context)

# def cancel_booking(request, event_slug):

#     event = Event.objects.get(slug=event_slug)
#     #retrieve number of tickets from the form to be cancelled
#     event.cancel_booking(#pass the number here)


#     if request.method == "POST":
#         form = CancelBookForm(request.POST)
#         if form.is_valid():
#             cancelled_tickets = form.save(commit = False)
#             if (cancelbooking.tickets >= cancelled_tickets):
#                 book.save()
#                 messages.success(request, "Successfully cancelled your booking!")
#                 return redirect ('dashboard')
#             messages.warning(request, "Check number of tickets booked and try again.")           
#     return redirect ("dashboard")












