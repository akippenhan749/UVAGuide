from calendar import HTMLCalendar

from .models import Event
#Parts of this code is modified code 
#Title: How to Create a Calendar Using Django
#Author: Hui Wen
#Date: 24 July, 2018
#URL: https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, user=None):
        self.user = user
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events, user):
        events_per_day = events.filter(start_time__day=day)
        user_events_per_day = events_per_day.filter(assigned_user = user)
        d = ''
        d += f'<a class="btn btn-info left" href="/cal/calendar/{self.month}-{day}-{self.year}"> {day}</a>'
        for event in user_events_per_day:
            d += f'<li> <a href="{event.title}@@{event.start_time}"/> {event.title} {(str(event.start_time))[11:16]}</a><br></li>'

        if day != 0:
            return f"<td><span class='date'></span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events, user):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, user)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, user, withyear=True):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, user)}\n'
        return cal
