from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import *
from .mixins import directions
from .models import *
from .utils import Calendar
from .views import *
import calendar

from django.urls import reverse


def index(request):
    template_name = 'map/index.html'
    return render(request, template_name)


'''
Maps views
'''

'''
Parts of this code is modified code 
Title: How to Create a Calendar Using Django
Author: Hui Wen
Date: 24 July, 2018
URL: https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
'''


def route(request):
    context = {"google_api_key": settings.GOOGLE_API_KEY}
    return render(request, 'map/route.html', context)


def maps(request):
    lat_a = request.GET.get("lat_a")
    long_a = request.GET.get("long_a")
    lat_b = request.GET.get("lat_b")
    long_b = request.GET.get("long_b")

    context = {
        "google_api_key": settings.GOOGLE_API_KEY,
        "lat_a": lat_a,
        "long_a": long_a,
        "lat_b": lat_b,
        "long_b": long_b,
        "origin": f'{lat_a}, {long_a}',
        "destination": f'{lat_b}, {long_b}',
        "directions": directions(lat_a=lat_a, long_a=long_a, lat_b=lat_b, long_b=long_b),
    }
    return render(request, 'map/maps.html', context)


'''End maps and Start Calendar'''


def DirectionsFormView(request):
    form = DirectionsForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('map/directionsform.html')
    else:
        form = DirectionsForm()
    return render(request, 'map/directionsform.html', {'form': form})


def eventDetails(request, eventTitle):
    template_name = 'cal/eventDetails.html'
    constraints = eventTitle.split("@@")
    time, event = constraints[1], constraints[0]
    starttime = Event.objects.filter(start_time = time)
    userID = starttime.filter(assigned_user = request.user.id)
    return render(request, template_name, {'event': userID.get(title=event)})


def get_day(request, month, day, year):
    template_name = 'cal/day.html'
    thisDate = datetime(year, month, day).isoformat()[0:10]
    #  current_user = request.user
    # print (current_user.id)
    allEvents = Event.objects.filter(assigned_user = request.user.id)
    eventList = []
    for event in allEvents:
        if str(event.start_time)[0:10] == thisDate:
            eventList.append(event)
    # eventList = Event.objects.get(start_time=thisDate)
    # print("THIS IS WHERE STUFF IS PRINTING", eventList)
    return render(request, template_name, {'events': eventList})

def routeAutofilled(request,inputLocation):
    template_name = 'map/routeAutofilled.html'
    inLocation = Event.objects.filter(location = inputLocation)[0]
    lat_a = request.GET.get("lat_a")
    long_a = request.GET.get("long_a")
    lat_b = request.GET.get("lat_b")
    long_b = request.GET.get("long_b")
    context = {'fillRoute' : inLocation,
    "google_api_key": settings.GOOGLE_API_KEY,
        "lat_a": lat_a,
        "long_a": long_a,
        "lat_b": lat_b,
        "long_b": long_b,
        "origin": f'{lat_a}, {long_a}',
        "destination": f'{lat_b}, {long_b}',
        "directions": directions(lat_a=lat_a, long_a=long_a, lat_b=lat_b, long_b=long_b),}
    return render(request, template_name, context)

def routeEventAutofilled(request,inputLocationEvent):
    template_name = 'map/routeAutofilled.html'
    inLocation = Event.objects.filter(location = inputLocationEvent)[0]
    lat_a = request.GET.get("lat_a")
    long_a = request.GET.get("long_a")
    lat_b = request.GET.get("lat_b")
    long_b = request.GET.get("long_b")
    context = {'fillRoute' : inLocation,
    "google_api_key": settings.GOOGLE_API_KEY,
        "lat_a": lat_a,
        "long_a": long_a,
        "lat_b": lat_b,
        "long_b": long_b,
        "origin": f'{lat_a}, {long_a}',
        "destination": f'{lat_b}, {long_b}',
        "directions": directions(lat_a=lat_a, long_a=long_a, lat_b=lat_b, long_b=long_b),}
    return render(request, template_name, context)


class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        user = self.request.user.id

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month, user)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(user,withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def event(request, event_id=None):
    instance = Event(assigned_user = request.user.id)
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event(assigned_user = request.user.id)

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})

def deleteEvent(request,event):
    constraints = event.split("@")
    deletingEvent = Event.objects.filter(title = constraints[0])
    check = deletingEvent.filter(location = constraints[1])
    check.delete()
    return render(request, 'cal/delete.html')



def profile(request):
    instance = StudentProfile(assigned_user = request.user.id)
    profile = StudentProfile.objects.filter(assigned_user = request.user.id)
    # print(request.user.id)
    if len(profile) == 0:
        # print("it gets here 1")
        if request.method == 'POST':
            # print("it gets here 3")
            p_form = ProfileUpdateForm(request.POST or None,request.FILES, instance = instance)
            if p_form.is_valid():
                p_form.save()
                return redirect('/map/profiles')
        else:
            p_form = ProfileUpdateForm()
        context={'p_form': p_form}
        return render(request, 'profile/profile.html',context)
    else:
        # if request.method == 'POST':
            p_form = ProfileUpdateForm(request.POST or None, request.FILES, instance = instance)
            # if p_form.is_valid():
            #     print("does it go here")
            #     print(request)
            #     p_form.save()
            #     return redirect('/profile/editprofile')
            # else:
            #     p_form = ProfileUpdateForm()
            context = {'p_form' : p_form, 'profile' : profile[0]}
            if(request.POST and p_form.is_valid()):
                # print("why") 
                profile[0].delete()
                p_form.save()
                return redirect('/map/profiles')
            
            return render(request, 'profile/editprofile.html', context)

        # update profile
    

   

# @login_required
# def editprofile(request, id):
#     template_name = 'editprofile.html'
#     obj = get_object_or_404(StudentProfile, id=id)

#     form = ProfileUpdateForm(request.POST or None, instance = obj)
#     context = {'form' : form}

#     if form.is_valid():
#         obj = form.save(commit = False)
#         obj.save()
#         messages.success(request, "You have updated your profile.")
#         context = {'form' : form}
#         return render(request, template_name, context)
#     else:
#         context = {'form' : form, 'error': 'Profile was not updated, please enter all fields.'}
#         return render(request, template_name, context)





def all_profiles(request):
    template_name = 'map/profiles.html'
    if request.method == 'POST':
        all_profiles = StudentProfile.objects.all()
    else:
        all_profiles = StudentProfile.objects.all()
    userList = []
    for user in all_profiles:
        userList.append(user)
    return render(request, template_name, {'profiles' : userList})

def existingProfile(request, username):
    template_name = 'map/profileDetails.html'
    return render(request, template_name, {'profile': StudentProfile.objects.get(username = username)})


