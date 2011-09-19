from django.contrib import admin
from course_tracker.department.models import *

admin.site.register(Institution)
admin.site.register(School)

class DepartmentAdmin(admin.ModelAdmin):
    save_on_top = True    
    list_display = ( 'name',  'abbreviation', 'school', 'institution',)
    search_fields = ( 'name',  'abbreviation',)
    list_filter = ('institution', 'school', )
admin.site.register(Department, DepartmentAdmin)
#admin.site.register(Department)

