from django.db import models
from django.contrib.localflavor.us.models import USStateField
from django.template.defaultfilters import slugify


class Building(models.Model):
    """Building Name, Nickname, and Address
    e.g. Northwest Building, NW, etc, etc"""
    abbrev = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=255)
    
    addr1 = models.CharField(max_length=255)
    addr2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = USStateField()
    zipcode = models.CharField(max_length=25)


    def __unicode__(self):
        return '%s, %s, %s %s %s' % (self.name, self.addr1, self.city, self.state, self.zipcode)

    class Meta:
        ordering = ('name',)

    def address_col_multiline(self):
       if self.addr2:
           return '%s<br />%s<br />%s<br />%s, %s %s' % (self.name, self.addr1, self.addr2, self.city, self.state, self.zipcode)
       else:
           return '%s<br />%s<br />%s, %s %s' % (self.name, self.addr1, self.city, self.state, self.zipcode)
    address_col_multiline.allow_tags = True
    
    def address_col(self):
        if self.addr2:
            return '%s, %s, %s, %s %s %s' % (self.name, self.addr1, self.addr2, self.city, self.state, self.zipcode)
        else:
            return '%s, %s, %s %s %s' % (self.name, self.addr1, self.city, self.state, self.zipcode)

    def address_col_xls(self):
        if self.addr2:
            return '%s\n%s\n%s\n%s\n%s' % (self.addr1, self.addr2, self.city, self.zipcode, self.state)
        else:
            return '%s\n%s\n%s\n%s' % ( self.addr1, self.city, self.zipcode, self.state)

class RoomType(models.Model):
    name = models.CharField(max_length=125)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class RoomDetail(models.Model):
    name = models.CharField(max_length=125)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        
class Room(models.Model):
    building = models.ForeignKey(Building)

    room_number = models.CharField('Room Name/Number', max_length=70)
    #abbreviation = models.CharField('Abbreviation', max_length=40)
    room_type = models.ForeignKey(RoomType)

    capacity = models.IntegerField()
    room_setup = models.CharField(max_length=255, blank=True)

    room_details = models.ManyToManyField(RoomDetail, blank=True, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.room_number, self.building)

    class Meta:
        ordering = ('building', 'room_number',)

    def building_abbrev(self):
        if self.building:
            return self.building.abbrev
        return ''

    def address_col_multiline(self):
        return '%s<br />%s' % (self.room_number, self.building.address_col_multiline())
    address_col_multiline.allow_tags = True

