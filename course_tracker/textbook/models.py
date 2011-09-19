from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    description = models.TextField('description/notes', blank=True)

    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ('name',)

class Author(models.Model):
    fname = models.CharField('First name', max_length=50)
    lname = models.CharField('Last Name', max_length=50)
    mi = models.CharField('Middle initials', max_length=15, blank=True, help_text='Include punctuation, such as the "." in "M."')

    def __unicode__(self):
        if self.mi:
            return '%s, %s %s' % (self.lname, self.fname, self.mi)
        else:
            return '%s, %s' % (self.lname, self.fname)

    class Meta:
        ordering = ('lname', 'fname', )


class Book(models.Model):
    title = models.CharField(max_length=255)
    edition = models.CharField(max_length=100, blank=True)
    publisher = models.ForeignKey(Publisher)
    authors = models.ManyToManyField(Author)
    catalog_number = models.CharField(max_length=20, blank=True)
    isbn = models.CharField('ISBN', max_length=13, help_text='Either 10 or 13 characters', blank=True)
    link = models.URLField(blank=True)
    
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.course_id, self.title)

    def hollis_listing(self):
        if self.isbn:
            return '<a href="http://hollis.harvard.edu/result.ashx?q=isbn:%s">check hollis</a>' % (self.isbn,)
        return '(n/a)'
    hollis_listing.allow_tags = True
    
    def amazon_listing(self):
        if self.isbn:
            return '<a href="http://www.amazon.com/gp/search/ref=sr_adv_b/?field-isbn=%s">check hollis</a>' % (self.isbn,)
        return '(n/a)'
    amazon_listing.allow_tags = True
    
    class Meta:
        ordering = ('title', 'edition')

class OnlineMaterial(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('title', 'link')

