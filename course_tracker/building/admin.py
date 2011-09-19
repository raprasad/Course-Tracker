from django.contrib import admin
from course_tracker.building.models import *

class BuildingAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display= ('name','abbrev',  'addr1', 'state', 'zipcode')
    search_fields = ('name', )
admin.site.register(Building, BuildingAdmin)

admin.site.register(RoomType)
admin.site.register(RoomDetail)


class RoomAdmin(admin.ModelAdmin):
    save_on_top = True    
    readonly_fields = ['address_col_multiline', 'building_abbrev',]
    list_display = ( 'room_number', 'building', 'room_type', 'capacity', 'room_setup',)
    list_filter = ( 'room_type', 'building','room_details',)
    fieldsets = [
     ('Location', { 'fields':  [  ('building', 'room_number',) ,\
                                    ('address_col_multiline', 'building_abbrev',), ]}), \
     ('Room Type/Capacity', { 'fields':  [  ( 'room_type', 'capacity',), 'room_setup'  ]}),\
     ('Room Details', { 'fields':  [  'room_details',]}),\
     ]
admin.site.register(Room, RoomAdmin)
