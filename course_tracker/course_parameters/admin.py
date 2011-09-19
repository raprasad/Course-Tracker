from django.contrib import admin
from course_tracker.course_parameters.models import *


admin.site.register(Requirement)
admin.site.register(CourseStatus)
admin.site.register(SectionStatus)
admin.site.register(CourseType)
admin.site.register(RoomStatus)
admin.site.register(CourseTerm)
admin.site.register(MeetingType)
