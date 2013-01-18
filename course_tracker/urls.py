from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
    # Example:
    (r'^course-tracker/course/', include('course_tracker.course.urls')),

    (r'^course-tracker/spreadsheets/', include('course_tracker.spreadsheet_helper.urls')),

    (r'^course-tracker/%s/'% (settings.TASTYPIE_URL_PIECE), include('course_tracker.course_info_api.urls_api')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Harvard Authz handler (callback after Authz login)
    (r'^course-tracker/hu-azp/', include('course_tracker.hu_authz_handler.urls')),

    # Uncomment the next line to enable the admin:
    (r'^course-tracker/control-panel/', include(admin.site.urls)),
    
    (r'^static/(?P<path>.*)$' , 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    
)

#if settings.DEBUG:
#    urlpatterns += patterns('',
#    (r'^media-course-tracker/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/rprasad/Local_Sites/course_tracker/media'}),
#)

urlpatterns += staticfiles_urlpatterns()
