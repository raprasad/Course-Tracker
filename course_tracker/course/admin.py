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
    readonly_fields = ( 'course_sort_field', 'instructor_history', 'enrollment_history','budget_history' , 'q_score_history')
    fieldsets = [
     ('Course', { 'fields':  [  ('course_id', 'course_sort_field',), 'title', 'catalog_number', \
                    'department', 'course_type', 'status' ]}), \
            
    ('Semester History - Click on a specific "Semester" for details.', { 'fields':  [ 'instructor_history', 'enrollment_history', 'budget_history', 'q_score_history' ]}),\
    #'enrollment_history', 'instructor_history', 
    #('Enrollment', { 'fields':  [  'enrollment_chart',  ]}),\
                    ]
admin.site.register(Course, CourseAdmin)

admin.site.register(SemesterInstructorQScore)

class SemesterInstructorQScoreAdminInline(admin.TabularInline):
    model = SemesterInstructorQScore
    #form = SemesterInstructorQScoreForm
    extra=0


class SemesterInstructorCreditAdminInline(admin.TabularInline):
    model = SemesterInstructorCredit
    extra=0
    

class CourseDevelopmentCreditAdminInline(admin.TabularInline):
    model = CourseDevelopmentCredit
    extra=0


class SemesterDetailsAdmin(admin.ModelAdmin):
    save_on_top = True    
    inlines = (SemesterInstructorQScoreAdminInline, SemesterInstructorCreditAdminInline, CourseDevelopmentCreditAdminInline )
    readonly_fields = ['course_link','instructors_list', 'course_title', 'instructor_history', 'budget_history', 'enrollment_history', 'q_score_history']
    list_display = ( 'course', 'year', 'term','time_sort','instructors_list', 'meeting_date', 'meeting_time', 'room', 'number_of_sections',  )
    list_filter = (  'year', 'term', 'meeting_type', 'course__department__name', 'instructors' )

    search_fields = ('course__title', 'instructors__lname', 'instructors__fname')
    filter_horizontal = ('instructors', 'teaching_assistants', 'requirements_met', )
    fieldsets = [
     ('Course', { 'fields':  [  ('course',) \
                ,  ('course_title', 'course_link',)\
                , ('year', 'term', 'time_sort', ), ]}), \
     ('Meeting Date', { 'fields':  [   ('meeting_type', 'enrollment_limit',), ('meeting_date', 'meeting_time', ), 'meeting_note', 'exam_group'  ]}),\
     
     ('Room', { 'fields':  [  ('room', 'confirmation_status',  )  ]}),\
     ('Sections', { 'fields':  [  ( 'number_of_sections', 'section_status', 'section_note',),   ]}),\

     ('Instructors', { 'fields':  [  'instructors', 'teaching_assistants', ]}),\


     ('Description / Prerequisites /Recommendations', {'classes': ('xcollapse',), 'fields':  [ 'description', 'prerequisites', 'recommendations',   ]}),\




     ('Requirements', { 'fields':  [  'mcb_required', 'requirements_met',   ]}),\

       ('Enrollments', { 'fields':  [ 'enrollments_entered', ( 'undergrads_enrolled', 'grads_enrolled', 'employees_enrolled', 'cross_registered', ),'withdrawals', 'total_enrolled',  ]}),\

     ('Budget', { 'fields':  [  ('budget', 'budget_note',) ]}),\

     ('Instructor/Enrollment/Budget History', { 'classes': ('xcollapse',), 'fields':  [ 'instructor_history', 'enrollment_history', 'budget_history', 'q_score_history' ]}),\

     ('"Q" Score for Semester', { 'fields':  [  ('q_score', ),   ]}),\


     ]
admin.site.register(SemesterDetails, SemesterDetailsAdmin)
