from django import forms
from course_tracker.instructor.models import *
from django.forms.widgets import TextInput
#, PasswordInput, HiddenInput, MultipleHiddenInput, \
#        FileInput, CheckboxInput, Select, NullBooleanSelect, SelectMultiple, \
#        DateInput, DateTimeInput, TimeInput, SplitDateTimeWidget, SplitHiddenDateTimeWidget, PasswordInput

from django.contrib.auth.models import User, Group

class InstructorAdminForm(forms.ModelForm):

    class Meta:
        widgets = {'mi': forms.TextInput(attrs={'size': 7})\
                    , 'fname': forms.TextInput(attrs={'size': 20}) \
                    , 'lname': forms.TextInput(attrs={'size': 20}) \
                    , 'room': forms.TextInput(attrs={'size': 20}) \
                    , 'room2': forms.TextInput(attrs={'size': 20}) \

                }
