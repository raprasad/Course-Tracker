from django.contrib import admin
from course_tracker.academic_year_credit.models import Position, AcademicYearCredit


admin.site.register(Position)

class AcademicYearCreditAdmin(admin.ModelAdmin):
    save_on_top = True    
    list_display = ( 'instructor',  'position', 'credit_score', 'year', 'term', 'time_sort')
    list_filter = ('year', 'term', 'instructor', 'position',  )
    search_fields = ('first_name', 'position__name', 'credit_score', 'instructor__lname', 'instructor__fname' )
    fieldsets = [ ('', { 'fields':  [  'instructor', 'position', ('year', 'term', 'time_sort', ), 'credit_score', 'note'  ]}), \
      ]
admin.site.register(AcademicYearCredit, AcademicYearCreditAdmin)

