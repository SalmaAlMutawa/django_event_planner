from django.urls import path
from .views import Login, Logout, Signup, home

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('events/list/', Logout.as_view(), name='events-list'),

    # path('event/create/', Logout.as_view(), name='events-list'),
    # path('events/list/', Logout.as_view(), name='dashboard'),
    # path('events/list/', Logout.as_view(), name='event-detail'),
]