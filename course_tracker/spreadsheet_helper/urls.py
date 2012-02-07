from django.conf.urls.defaults import *

# lab member xls file - button in the admin
urlpatterns = patterns(
    'spreadsheet_helper.views_enrollment'
,    url(r'^enrollment/xls/$', 'view_course_enrollments', name='view_course_enrollments' )

,    url(r'^enrollment-mcb/xls/$', 'view_mcb_related_course_enrollments', name='view_mcb_related_course_enrollments' )


,
)

