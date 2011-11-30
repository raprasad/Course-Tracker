from django.conf.urls.defaults import *

# lab member xls file - button in the admin
urlpatterns = patterns(
    'course_tracker.course.view_xls'
,    url(r'^enrollment/xls/$', 'view_course_enrollments', name='view_course_enrollments' )
,
)

