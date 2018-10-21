from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Event


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
            return redirect("home")
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
                return redirect('dashboard')
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
    my_events = Event.objects.filter(organizer=user)

    context = {
        "my_events" : my_events 
    }
    return render (request, 'dashboard.html', context)

def create_event (request):
    # if request.user.is_anonymous:
    #     return redirect ('login')
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
    events = Event.objects.all()
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

def event_detail (request, event_id):
    event = Event.objects.get(id=event_id)

    context = {
        "event" : event,
    }

    return render (request, 'event_detail.html', context)









