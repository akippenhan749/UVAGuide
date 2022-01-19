from django.db.models import CharField, Model, DateTimeField, TextField, IntegerField, ForeignKey
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from django.urls import reverse
from django.template.defaultfilters import slugify


class Directions(Model):
    profile = CharField(max_length=100)
    cords = CharField(max_length=100)

    def __str__(self):
        return self.profile


class Event(Model):
    title = CharField(max_length=200)
    location = CharField(max_length=200)
    start_time = DateTimeField()
    end_time = DateTimeField()
    assigned_user = IntegerField(null = True, blank = False, default = 0)

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

#This is an unused model
class Class(Model):
    title = CharField(max_length=200)
    code = CharField(max_length=50)
    location = CharField(max_length=200)
    professor = CharField(max_length=200)
    description = TextField()
    start_time = DateTimeField()
    end_time = DateTimeField()


        
class StudentProfile(Model):
    name = CharField(max_length=100)
    username = CharField(max_length=50, default = '')
    email = CharField(max_length=50, default = '')
    major = CharField(max_length=100)
    bio = TextField(max_length=500)
    assigned_user = IntegerField(null = True, blank = False, default = 0)
    
    
    
# class StudentUser(Model):
