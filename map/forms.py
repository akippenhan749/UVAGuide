from django.forms import ModelForm, Select, Textarea, DateInput, HiddenInput

from .models import *


class DirectionsForm(ModelForm):
    class Meta:
        model = Directions
        fields = '__all__'
        widgets = {
            'profile': Select(attrs={'walking', 'cycling', 'driving'}),
            'cords': Textarea(),
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'), 
            # 'assigned_user': HiddenInput(),
        }
        fields = ['title', 'location', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('instance', None)
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

    # def setUser(self,user):
    #     self.fields['assigned_user'].queryset = user
        # self.fields['assigned_user'] = user.objects.get(id = 2)
    # def save(self, *args, **kwargs):
    #     kwargs['commit'] = False
    #     obj = super(EventForm, self).save(*args, **kwargs)
    #     if self.request:
    #         obj.user = self.request.user
    #     obj.save()
    #     return obj
    
# class UserUpdateForm(ModelForm):
#     class Meta:
#         model = StudentUser
#         fields='__all__'
        
class ProfileUpdateForm(ModelForm):
    class Meta:
        model = StudentProfile
        fields=['name', 'username', 'email', 'major', 'bio']