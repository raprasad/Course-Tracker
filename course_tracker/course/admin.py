from django.contrib import admin
from course_tracker.course.models import *
from course_tracker.course.forms import *

class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    
    save_on_top = True  
    list_display = ( 'course_id', 'title', 'catalog_number' )
    search_fields = ( 'course_id', 'title', 'catalog_number', )
    list_filter = ('status',)
    
    #readonly_fields = ('semester_details', 'enrollment_chart','course_sort_field',  )
    readonly_fields = ('semester_details', 'course_sort_field',  )
    fieldsets = [
     ('Course', { 'fields':  [  ('course_id', 'course_sort_field',), 'title', 'catalog_number', \
                    'department', 'course_type', 'status' ]}), \
            
    ('Semester Details', { 'fields':  [  'semester_details',  ]}),\
    #('Enrollment', { 'fields':  [  'enrollment_chart',  ]}),\
                    ]
admin.site.register(Course, CourseAdmin)


class SemesterInstructorQScoreAdminInline(admin.TabularInline):
    model = SemesterInstructorQScore
    #form = SemesterInstructorQScoreForm
    extra=0
    

class SemesterDetailsAdmin(admin.ModelAdmin):
    save_on_top = True    
    inlines = (SemesterInstructorQScoreAdminInline, )
    readonly_fields = ['instructors_list', 'course_title', 'instructor_history', 'budget_history', 'enrollment_history', ]
    list_display = ( 'course', 'year', 'term','time_sort','instructors_list', 'meeting_date', 'meeting_time', 'room', 'number_of_sections',  )
    list_filter = (  'year', 'term', 'meeting_type', 'course__department__name', 'instructors' )

    search_fields = ('course__title', 'instructors__lname', 'instructors__fname')
    filter_horizontal = ('instructors', 'teaching_assistants', 'requirements_met', 'books',)
    fieldsets = [
     ('Course', { 'fields':  [  ('course',) ,  'course_title',('year', 'term', 'time_sort', ), ]}), \
     ('Meeting Date', { 'fields':  [   ('meeting_type', 'enrollment_limit',), ('meeting_date', 'meeting_time', 'through_reading_period',), 'meeting_note', 'exam_group'  ]}),\
     
     ('Room', { 'fields':  [  ('room', 'confirmation_status', 'visitors', )  ]}),\
     ('Sections', { 'fields':  [  ( 'number_of_sections', 'section_status', 'section_note',),   ]}),\

     ('Instructors', { 'fields':  [  'instructors', 'teaching_assistants', ]}),\


     ('Description / Prerequisites /Recommendations', {'classes': ('xcollapse',), 'fields':  [ 'description', 'prerequisites', 'recommendations',   ]}),\




     ('Requirements', { 'fields':  [  'mcb_required', 'requirements_met',   ]}),\

       ('Enrollments', { 'fields':  [ 'enrollments_entered', ( 'undergrads_enrolled', 'grads_enrolled', 'employees_enrolled', 'cross_registered', ),'withdrawals', 'total_enrolled',  ]}),\

     ('Budget', { 'fields':  [  ('budget', 'budget_note',) ]}),\

     ('Instructor/Enrollment/Budget History', { 'classes': ('xcollapse',), 'fields':  [ 'instructor_history', 'enrollment_history', 'budget_history',  ]}),\

     ('Books', { 'fields':  [  'books', ]}),\

     ('"Q" Score for Semester', { 'fields':  [  ('q_score', ),   ]}),\


     ]
admin.site.register(SemesterDetails, SemesterDetailsAdmin)
