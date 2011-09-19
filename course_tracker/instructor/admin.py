from django.contrib import admin
from course_tracker.instructor.models import *
from course_tracker.instructor.forms import *

admin.site.register(InstructorStatus)
admin.site.register(InstructorTitle)

#admin.site.register(AppointmentType)


admin.site.register(TeachingAssistant)
admin.site.register(LabAssistant)

class InstructorAdmin(admin.ModelAdmin):
    form = InstructorAdminForm
    save_on_top = True    
    readonly_fields = ['course_history', 'q_score_history',]
    
    list_display = ( 'last_name',  'first_name', 'title', 'status',)
    list_filter = ('status', 'title', 'primary_affiliation' )
    filter_vertical = ( 'primary_affiliation', 'other_affiliations', 'lab_assistants', )
    search_fields = ('first_name', 'last_name', 'title' 'primary_affiliation' )
    fieldsets = [
     ('Name / Title', { 'fields':  [ 'user', ('first_name', 'mi', 'last_name',), 'title' , ]}), \
     ('Appointment Types', { 'fields':  [ 'appointment_types'  ]}),\
     ('Affiliation', { 'fields':  [  'primary_affiliation', 'other_affiliations', ]}),\
     ('Lab Assistants', { 'fields':  [  'lab_assistants', ]}),\
     #('Q Score / Status', { 'fields':  [ 'q_score', 'status',  ]}),\
     ('Status', { 'fields':  [  'status',  ]}),\
     ('Offices', { 'fields':  [ ('room', 'building',),\
                                  ('room2', 'building2',),  ]}),\
     ('Email / Phone / Fax', { 'fields':  [ 'email', 'phone', 'fax',  ]}),\

     ('Three Year Plan', { 'fields':  [  'three_year_plan',  ]}),\
     ( 'Course History', { 'classes': ('xcollapse',), 'fields':  [ 'course_history', 'q_score_history',  ]}),\
     
     
     ]
admin.site.register(Instructor, InstructorAdmin)

