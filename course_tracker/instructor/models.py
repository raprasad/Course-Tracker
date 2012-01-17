from django.db import models
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.template.defaultfilters import slugify
from course_tracker.department.models import Department
from course_tracker.building.models import Building
from course_tracker.qscore_helper.q_score_stats_helper import QScoreStatsHelper


class InstructorStatus(models.Model):
    name = models.CharField('Teaching Status', max_length=75)
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Instructor status'


        
class InstructorTitle(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
"""
class AppointmentType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
"""
class TeachingAssistant(models.Model):
    user = models.ForeignKey(User, unique=True)

    first_name = models.CharField(max_length=255)
    mi = models.CharField('Middle Initial', max_length=10, blank=True)
    last_name = models.CharField(max_length=255)

    email = models.EmailField()
    description = models.TextField(blank=True)

    def first_name_last_name(self):
        if self.mi:
            return '%s %s %s' % (self.first_name, self.mi, self.last_name)
        
        return '%s %s' % (self.first_name, self.last_name)

    def save(self):
         super(TeachingAssistant, self).save()

         self.user.first_name = self.first_name
         self.user.last_name = self.last_name
         self.user.email = self.email
         self.user.save()
        
    def __unicode__(self):
        if self.mi:
            return '%s, %s %s' % (self.last_name, self.first_name, self.mi)
        return '%s, %s' % (self.last_name, self.first_name)

    class Meta:
        ordering = ('last_name', 'first_name', )

class LabAssistant(models.Model):
    user = models.ForeignKey(User, unique=True)

    first_name = models.CharField(max_length=255)
    mi = models.CharField('Middle Initial', max_length=10, blank=True)
    last_name = models.CharField(max_length=255)

    email = models.EmailField()
    description = models.TextField(blank=True)

    def first_name_last_name(self):
        if self.mi:
            return '%s %s %s' % (self.first_name, self.mi, self.last_name)
        
        return '%s %s' % (self.first_name, self.last_name)

    def save(self):
         super(LabAssistant, self).save()

         self.user.first_name = self.first_name
         self.user.last_name = self.last_name
         self.user.email = self.email
         self.user.save()
        
    def __unicode__(self):
        if self.mi:
            return '%s, %s %s' % (self.last_name, self.first_name, self.mi)
        return '%s, %s' % (self.last_name, self.first_name)

    class Meta:
        ordering = ('last_name', 'first_name', )    
     
        
class Instructor(models.Model):
    user = models.ForeignKey(User, unique=True)

    first_name = models.CharField(max_length=255)
    mi = models.CharField('Middle Initial', max_length=10, blank=True)
    last_name = models.CharField(max_length=255)
    
    email = models.EmailField()
    phone = PhoneNumberField('US Phone')
    fax = PhoneNumberField(blank=True)
    
    room = models.CharField(max_length=75)
    building = models.ForeignKey(Building)

    room2 = models.CharField(max_length=75, blank=True)
    building2 = models.ForeignKey(Building, blank=True, null=True, related_name='building 2')

    title = models.ForeignKey(InstructorTitle)
    appointment_types = models.TextField(blank=True) #ManyToManyField(AppointmentType, null=True, blank=True)#is_staff = models

    lab_assistants = models.ManyToManyField(LabAssistant, blank=True, null=True)

    primary_affiliation = models.ManyToManyField(Department)
    other_affiliations = models.ManyToManyField(Department, blank=True, null=True, related_name='other affiliations')

    #q_score = models.IntegerField()
    status = models.ForeignKey(InstructorStatus)
        
    def course_history(self):
        if not self.id or self.semesterdetails_set.count() ==0:
            return '(no history)'        
        lst = self.semesterdetails_set.all().order_by('-year','term')
                
        lu = {'semester_details' : lst   }
            
        return render_to_string('admin/instructor/course_history.html', lu)      
    course_history.allow_tags = True
    
    
    def q_score_history(self):
        """For displaying Q score of class as well as the instructor"""
        if not self.id or self.semesterinstructorqscore_set.count() ==0:
            return '(no history)'        
        
        # retrieve semesters where instructor taught
        lst = self.semesterdetails_set.all().order_by('-year','term') 
        if lst.count() == 0:
            return '(no history)'

        # retrieve instructor specific q scores
        sdict = {}  # { semester : SemesterInstructorQScore }
        for semester_qscore in self.semesterinstructorqscore_set.all():    
            sdict.update({ semester_qscore.semester : semester_qscore})

        # match instructor specific scores with semester
        updated_lst = []
        for semester_obj in lst:
            if sdict.has_key(semester_obj):
                semester_obj.instructor_specific_q_score = sdict.get(semester_obj).q_score
            else:
                semester_obj.instructor_specific_q_score = 0
            updated_lst.append(semester_obj)
        
        updated_lst = filter(lambda x: x.q_score > 0 or x.instructor_specific_q_score > 0 , updated_lst)

        q_scores_course = map(lambda x: x.q_score, updated_lst)
        q_scores_instructor = map(lambda x: x.instructor_specific_q_score, updated_lst)
        stats_helper = QScoreStatsHelper(q_scores_course)
        instructor_stats_helper = QScoreStatsHelper(q_scores_instructor)
        
        lu = { 'semester_details' : updated_lst\
            , 'stats_helper':stats_helper
            , 'instructor_stats_helper' :instructor_stats_helper }

        return render_to_string('admin/instructor/q_score_history.html', lu)      
    q_score_history.allow_tags = True
    

    def course_development_credit_score_history(self):
        #   coursedevelopmentcredit_set
        if not self.id or self.coursedevelopmentcredit_set.count()==0:
            return '(no history)'

        return render_to_string('admin/instructor/course_development_credit_score_history.html'\
                    , { 'course_dev_credit_score_history' : self.coursedevelopmentcredit_set.all()})
                          
    course_development_credit_score_history.allow_tags = True
    
    def academic_semester_credit_score_history(self):
        if not self.id or self.academicyearcredit_set.count()==0:
            return '(no history)'

        lu = { 'academic_credit_score_history' : self.academicyearcredit_set.all()}
        
        return render_to_string('admin/instructor/academic_semester_credit_score_history.html', lu )

    academic_semester_credit_score_history.allow_tags = True
    
    def credit_score_history(self):
        #   coursedevelopmentcredit_set
        if not self.id:
            return '(no history)'

        semester_credit_score_history = self.semesterinstructorcredit_set.all()

        lu = { 'semester_credit_score_history' : semester_credit_score_history}

        return render_to_string('admin/instructor/credit_score_history.html', lu)      
    credit_score_history.allow_tags = True
    
    
    def fname_lname(self):
        if self.mi:
            return '%s %s %s' % (self.first_name, self.mi, self.last_name)
        
        return '%s %s' % (self.first_name, self.last_name)
        
    def __unicode__(self):
        if self.mi:
            return '%s, %s %s' % (self.last_name, self.first_name, self.mi)
        return '%s, %s' % (self.last_name, self.first_name)

    def save(self):
         super(Instructor, self).save()

         self.user.first_name = self.first_name
         self.user.last_name = self.last_name
         self.user.email = self.email
         self.user.save()

    class Meta:
        ordering = ('last_name', 'first_name', )

