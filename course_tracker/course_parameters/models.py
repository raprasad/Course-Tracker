from django.db import models


class Requirement(models.Model):
    name = models.CharField(max_length=125)
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)

class CourseStatus(models.Model):
    name = models.CharField(max_length=75)
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Course status'

class SectionStatus(models.Model):
    name = models.CharField(max_length=75)
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Section status'

class CourseType(models.Model):
    """course type: e.g. full, half, quarter, etc"""
    name = models.CharField(max_length=75)
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('id',)

class RoomStatus(models.Model):
    name = models.CharField(max_length=75)
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Room status'


class CourseTerm(models.Model):
    name = models.CharField(max_length=75)
    sort_month = models.IntegerField(help_text='e.g. for Fall, enter "8" for August')
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('sort_month', 'name',)


class MeetingType(models.Model):
    name = models.CharField(max_length=75)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
