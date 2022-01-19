from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

from .views import *


login_patterns = ([
  path('logout', LogoutView.as_view()), ], 'login')

map_patterns = ([
    path('', route, name='route'),
    path('maps', maps, name='maps'),
    ], 'route')

cal_patterns = ([
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('delete/<str:event>', deleteEvent, name = 'delete'),
    path('event/new', event, name='new_event'),
    path('event/edit/', event, name='edit_event'),
    path('calendar/<int:month>-<int:day>-<int:year>', get_day, name='date'),
    path('calendar/<str:eventTitle>', eventDetails, name='eventDetails'), ], 'cal')

profile_patterns = ([
    path('', profile, name='profile'),
    # path('profile/', profile, name='profile'),
    # path('editprofile/', profile, name = 'editprofile'),
    #path('', user)
    ], 'profile')

urlpatterns = [
    path('', index, name='index'),
    path('', include(login_patterns)),
    path('route/', include(map_patterns)),
    path('cal/', include(cal_patterns)),
    path('accounts/', include('allauth.urls')),
    # path('profile/', include(profile_patterns)),
    path('profile/', profile, name='profile'),
    path('editprofile/', profile, name = 'editprofile'),
    path('profile/editprofile/', profile, name = 'profileeditprofile'),
    path('profiles/', all_profiles, name='profiles'),
    path('profiles/<str:username>', existingProfile, name= 'existingProfile'),
    path('route/<str:inputLocation>', routeAutofilled, name = 'routeAutofilled'),
    path('route/<str:inputLocation>', routeEventAutofilled, name = 'routeEventAutofilled'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
