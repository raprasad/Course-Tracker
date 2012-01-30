from django.contrib import admin
from course_tracker.course.models import *
from course_tracker.course.forms import *
import copy

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

class SemesterInstructorCreditAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ( 'semester', 'instructor', 'credit_score', 'note' )
admin.site.register(SemesterInstructorCredit, SemesterInstructorCreditAdmin)

class SemesterInstructorQScoreAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ( 'semester', 'instructor', 'q_score',  )
admin.site.register(SemesterInstructorQScore, SemesterInstructorQScoreAdmin)
    

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

def copy_semester(modeladmin, request, queryset):
    for sd in queryset:
        sd_copy = copy.copy(sd)
        sd_copy.id = None
        sd_copy.save()    
        
        # copy instructors
        for instructor in sd.instructors.all():
            sd_copy.instructors.add(instructor)
        sd_copy.save()

        # copy requirements_met
        for req in sd.requirements_met.all():
            sd_copy.requirements_met.add(req)
        sd_copy.save()
        
        # zero out enrollments
        for attr_name in ['enrollments_entered', 'undergrads_enrolled', 'grads_enrolled', 'employees_enrolled', 'cross_registered', 'withdrawals']:
            sd_copy.__dict__.update({ attr_name : 0})
        sd_copy.save()
            
    copy_semester.short_description = "Make a Copy of Semester Details"



class SemesterDetailsAdmin(admin.ModelAdmin):
    save_on_top = True    
    inlines = (SemesterInstructorQScoreAdminInline, SemesterInstructorCreditAdminInline, CourseDevelopmentCreditAdminInline )
    readonly_fields = ['course_link','instructors_list', 'course_title', 'instructor_history', 'budget_history', 'enrollment_history', 'q_score_history', 'created', 'last_update']
    list_display = ( 'course', 'year', 'term','time_sort','instructors_list', 'last_update','meeting_date', 'meeting_time', 'room', 'number_of_sections',  'last_update')
    list_filter = (  'year', 'term', 'meeting_type', 'course__department__name', 'instructors' )
    actions = [copy_semester]
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
