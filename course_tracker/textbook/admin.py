from django.contrib import admin
from course_tracker.textbook.models import *


admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)