from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
    # Example:
    (r'^course/', include('course_tracker.course.urls')),

    (r'^spreadsheets/', include('course_tracker.spreadsheet_helper.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Harvard Authz handler (callback after Authz login)
    (r'^hu-azp/', include('course_tracker.hu_authz_handler.urls')),

    # Uncomment the next line to enable the admin:
    (r'^control-panel/', include(admin.site.urls)),
        
)
