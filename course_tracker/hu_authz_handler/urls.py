from django.conf.urls.defaults import *


urlpatterns = patterns(
    'course_tracker.hu_authz_handler.views',

    url(r'^callback/$', 'view_handle_authz_callback', name='view_handle_authz_callback' ),

    #url(r'^log-out/$', 'view_logout_page', name='view_logout_page' ),

    #url(r'^log-out-success/$', 'view_logout_success', name='view_logout_success' ),


)

