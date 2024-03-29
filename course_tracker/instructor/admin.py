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
    readonly_fields = ['course_history', 'q_score_history', 'credit_score_history', 'course_development_credit_score_history', 'academic_semester_credit_score_history']
    
    list_display = ( 'last_name',  'first_name', 'title', 'status',)
    list_filter = ('status', 'title', 'primary_affiliation' )
    filter_vertical = ( 'primary_affiliation', 'other_affiliations',  )
    filter_horizontal = ('lab_assistants', )
    search_fields = ('first_name', 'last_name', 'title__name', 'primary_affiliation__name' )
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

     ( 'Course History', { 'classes': ('',), 'fields':  [ 'course_history', 'q_score_history',  ]}),\
     ( 'Credit Score History', { 'classes': ('',), 'fields':  [ 'credit_score_history',]}),\
     
     
     ]
admin.site.register(Instructor, InstructorAdmin)

