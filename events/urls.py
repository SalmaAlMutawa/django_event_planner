from django.urls import path
from events import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('events/', views.event_list, name='events-list'),
	path('create/', views.create_event, name='create-event'),
    path('detail/<event_slug>', views.event_detail, name='event-detail'),
    # path('events/list/', Logout.as_view(), name='dashboard'),
