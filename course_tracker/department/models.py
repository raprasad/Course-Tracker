from django.db import models

class Institution(models.Model):
    """e.g. Harvard University"""
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Institution'
        verbose_name_plural = verbose_name

class School(models.Model):
    """e.g. FAS, HMS, etc"""
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'School'
        verbose_name_plural = verbose_name


class Department(models.Model):
    """e.g. Department of Molecular & Cellular Biology"""
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=20, unique=True)
    school = models.ForeignKey(School, blank=True, null=True, help_text='optional')
    institution = models.ForeignKey(Institution)
    
    def __unicode__(self):
        if self.school:
            return '%s (%s), %s, %s' % (self.name, self.abbreviation, self.school, self.institution)
            
        return '%s (%s), %s' % (self.name, self.abbreviation, self.institution)

    class Meta:
        ordering = ('abbreviation', 'name',)
        unique_together = ('name', 'school', 'institution',)