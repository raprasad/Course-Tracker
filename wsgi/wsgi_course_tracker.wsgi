import os
import sys

sys.stdout = sys.stderr     # send print statements to the apache logs

prod_paths = ['/var/webapps/django/Course-Tracker'\
    , '/var/webapps/django/Course-Tracker/course_tracker']

for p in prod_paths:
    if os.path.isdir(p): 
        sys.path = [p] + sys.path
        # sys.path.append(p)

os.environ['DJANGO_SETTINGS_MODULE'] = 'course_tracker.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

