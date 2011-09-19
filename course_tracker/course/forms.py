from django import forms
from course_tracker.course.models import *
from django.forms.widgets import TextInput
#, PasswordInput, HiddenInput, MultipleHiddenInput, \
#        FileInput, CheckboxInput, Select, NullBooleanSelect, SelectMultiple, \
#        DateInput, DateTimeInput, TimeInput, SplitDateTimeWidget, SplitHiddenDateTimeWidget, PasswordInput

class CourseAdminForm(forms.ModelForm):

    class Meta:
        widgets = {'title': forms.TextInput(attrs={'size': 70})\
                    #, 'fname': forms.TextInput(attrs={'size': 20}) \
                    #, 'lname': forms.TextInput(attrs={'size': 20}) \
                    #, 'room': forms.TextInput(attrs={'size': 20}) \
                    #, 'room2': forms.TextInput(attrs={'size': 20}) \

                }

class SemesterInstructorQScoreForm(forms.ModelForm):

    def clean(self):
        """Make sure that the chosen instructor is one of those specified for the given semester"""
        semester = self.cleaned_data.get('semester', None)
        instructor = self.cleaned_data.get('instructor', None)

        if semester is None:
            raise forms.ValidationError('Please choose a semester')

        if instructor is None:
            raise forms.ValidationError('Please choose an instructor')
        
        if semester.instructors.count() == 0:
            pass
        elif not instructor in semester.instructors.all():
            self._errors['instructor'] = self.error_class(['That instructor is not selected to teach this semester.'])
            raise forms.ValidationError('Please choose an instructor')

        return self.cleaned_data

