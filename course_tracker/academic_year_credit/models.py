from django.db import models
import datetime

from course_tracker.course_parameters.models import CourseTerm
from course_tracker.instructor.models import Instructor, TeachingAssistant


class Position(models.Model):   
    # e.g. Tutor, Department Head, etc.
    name = models.CharField(max_length=75)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)



class AcademicYearCredit(models.Model):
    """
    Semester-specific credit information not related to a particular course.    
    """
    instructor = models.ForeignKey(Instructor)
    position = models.ForeignKey(Position)
    credit_score = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    year = models.IntegerField()
    term = models.ForeignKey(CourseTerm)
    time_sort = models.DateField(help_text='auto-filled on save', blank=True, null=True)
    note = models.CharField(max_length=255, blank=True)

    def save(self):
        # set the "time_sort" variable
        try:
           self.time_sort = datetime.date(self.year, self.term.sort_month, 1)
        except:
           self.time_sort = None
   
        super(AcademicYearCredit, self).save()

    class Meta:
        ordering = ('-time_sort', 'instructor')
        