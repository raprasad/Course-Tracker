from django.contrib import admin
from course_tracker.course_parameters.models import *


admin.site.register(Requirement)
admin.site.register(CourseStatus)
admin.site.register(SectionStatus)
admin.site.register(CourseType)
admin.site.register(RoomStatus)

class CourseTermAdmin(admin.ModelAdmin):
    save_on_top = True  
    list_display = ( 'name', 'sort_month',)
admin.site.register(CourseTerm, CourseTermAdmin)

admin.site.register(MeetingType)
