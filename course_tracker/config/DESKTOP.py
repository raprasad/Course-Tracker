# rprasad/123
import os

CURRENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
FILES_TO_SERVE_ROOT = '/Users/rprasad/mcb-git/Course-Tracker/files_to_serve' 
FILES_TO_SERVE_URL_BASE = 'http://127.0.0.1:8000/' #'mcbweb.rc.fas.harvard.edu/mcb/'
#os.path.join(CURRENT_DIR, 'mcb_files_to_serve')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Raman Prasad', 'raman_prasad@harvard.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': os.path.join(CURRENT_DIR, 'db', 'cdb_01.db3'),                               
        'USER': '',                   
        'PASSWORD': '', 
        'HOST': '',   
        'PORT': '', 
    }
}


EMAIL_HOST = 'mail.fas.harvard.edu'
EMAIL_HOST_USER = 'raman_prasad@harvard.edu'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/Users/rprasad/mcb-git/Course-Tracker/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media-course-tracker/'

# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

SESSION_COOKIE_NAME = 'course_tracker_desktop'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(FILES_TO_SERVE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = FILES_TO_SERVE_URL_BASE + 'static/'

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(CURRENT_DIR, 'static_site_files'),)


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(FILES_TO_SERVE_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = '/media-course-tracker/'
MEDIA_URL = FILES_TO_SERVE_URL_BASE + 'media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'djj-7@_bjjd&r@bl8oz01(gq%zyi8h*ve35kd7d@ier_1x((qe'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'course_tracker.urls'

TEMPLATE_DIRS = (
    os.path.join(CURRENT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',

    'course_tracker.building',
    'course_tracker.department',
    'course_tracker.instructor',
    #'course_tracker.textbook',
    'course_tracker.course_parameters',
    'course_tracker.course',
    'course_tracker.academic_year_credit',
    'course_tracker.spreadsheet_helper',
    
    # Uncomment the next line to enable the admin:

    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)



