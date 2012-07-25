import django   # version needed to switch between 1.3/1.4

# Django settings for course_tracker project.

import socket

if socket.gethostname() == 'Raman-Prasad-Desktop-Mac.local':
    import config.DESKTOP as config
elif socket.gethostname() == 'mcb-adminapps.unix.fas.harvard.edu':
    import config.prod_fas as config
    #    server_ip_address = socket.gethostbyname(socket.gethostname())
else:
    import sys
    print 'Config file not found for host [%s] ip [%s]' % (socket.gethostname(), server_ip_address)
    sys.exit(0)

DEBUG = config.DEBUG
TEMPLATE_DEBUG = config.TEMPLATE_DEBUG

ADMINS = config.ADMINS

MANAGERS = ADMINS

DATABASES = config.DATABASES

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

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

SESSION_COOKIE_NAME = config.SESSION_COOKIE_NAME

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT =  config.MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = config.MEDIA_URL


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = config.STATIC_ROOT

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = config.STATIC_URL

# Additional locations of static files
STATICFILES_DIRS = config.STATICFILES_DIRS

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".

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

INTERNAL_IPS = ('140.247.108.24', '127.0.0.1', )

ROOT_URLCONF = config.ROOT_URLCONF

TEMPLATE_DIRS = config.TEMPLATE_DIRS

INSTALLED_APPS = config.INSTALLED_APPS


SESSION_COOKIE_NAME = 'mcb_course_tracker'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SMTP_CONNECTION_STRING = 'mail.fas.harvard.edu' 
EMAIL_HOST = 'mail.fas.harvard.edu' 
