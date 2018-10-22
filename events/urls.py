from django.urls import path
from events import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
	path('',views.home, name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('events/', views.event_list, name='events-list'),
	path('create/', views.create_event, name='create-event'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('detail/<slug:event_slug>/', views.event_detail, name='event-detail'),

    path('edit/<slug:event_slug>/', views.event_edit, name='event-edit'),
    path('delete/<slug:event_slug>/', views.event_delete, name='event-delete'),
    path('book/<slug:event_slug>/', views.event_book, name='event-book'),

]