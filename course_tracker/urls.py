from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^course/', include('course_tracker.course.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^course-tracker/control-panel/', include(admin.site.urls)),
    
    (r'^media-course-tracker/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/rprasad/Local_Sites/course_tracker/media'}),
        
)
