from django.db import models
from django.template.loader import render_to_string
from django.db.models.signals import post_save      

import datetime
import re

from course_tracker.department.models import Department
from course_tracker.building.models import Room
from course_tracker.instructor.models import Instructor, TeachingAssistant
from course_tracker.course_parameters.models import *
#from course_tracker.textbook.models import Book



class Course(models.Model):
    """
    Basic Course information that doesn't change from semester to semester
    """
    course_id = models.CharField(max_length=20)
    
    course_sort_field = models.CharField(max_length=30, blank=True, help_text='auto-filled on save')
    
    title = models.CharField(max_length=255)
    catalog_number = models.CharField(max_length=20)
    course_type = models.ForeignKey(CourseType)
    department = models.ForeignKey(Department)
    status = models.ForeignKey(CourseStatus)
    
    def semester_details(self):
         return '(coming soon!)'
         lst = SemesterDetails.objects.filter(course=self).order_by('-year', 'term')
         if lst.count() == 0:
             return '(no history)'
         return render_to_string('admin/course/semesterdetails/budget_history.html', { 'semester_details' : lst })      
    semester_details.allow_tags = True
    
    """
    def enrollment_chart(self):
        lst = SemesterDetails.objects.filter(course=self).order_by('-year', 'term')
        if lst.count() == 0:
             return '(no history)'
        return render_to_string('admin/course/course/enrollment_chart.html', { 'semester_details' : lst })      
    enrollment_chart.allow_tags = True
    """

    def enrollment_chart(self):
        lu = { 'categories' : [ 'Fall 2008', 'Spring 2009','Fall 2009', 'Spring 2010', 'Fall 2010', 'Spring 2011'],\
             'undergrad' : [18, 22, 30, 34, 40, 47],\
             'grad' : [1, 2, 4, 4, 5, 7],\
             'employee' : [2, 3, 0, 1, 1, 2] }
        lu['total_enrolled'] = [sum(a) for a in zip(lu['undergrad'], lu['grad'],lu['employee'])]

        return render_to_string('admin/course/course/enrollment_chart.html', lu )
    enrollment_chart.allow_tags = True
    
    def __unicode__(self):
        return '%s - %s' % (self.course_id, self.title)
    
    def format_course_number_for_sorting(self):
        """Pad the 2nd number"""
        if not self.course_id:
            return 0
        course_id_parts = self.course_id.split()    # e.g., split "MCB 201r" to "MCB" and "201r"
        last_part = course_id_parts[-1]             # e.g. 201r
        last_part = re.sub("\D", "", last_part)   # 201r -> 201
        last_part = last_part.zfill(5)
        if len(last_part) == 0:
            return 0

        end_letter = self.course_id[-1]
        if end_letter.isdigit():
            end_letter = ''
        return '%s %s%s' % (' '.join(course_id_parts[:-1]), last_part, end_letter)
    
    
    def save(self):
        self.course_sort_field = self.format_course_number_for_sorting()
        super(Course, self).save()
        
    class Meta:
        ordering = ('course_sort_field', 'course_id',)
        


class SemesterDetails(models.Model):
    """
    Semester-specific information for a particular course.    
    """
    course = models.ForeignKey(Course)

    enrollment_limit = models.IntegerField(null=True, blank=True)

    year = models.IntegerField()
    term = models.ForeignKey(CourseTerm)
    time_sort = models.DateField(help_text='auto-filled on save', blank=True, null=True)
    
    q_score = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    number_of_sections = models.IntegerField(default=0)
    section_status = models.ForeignKey(SectionStatus)
    section_note = models.TextField(blank=True)
    
    meeting_type = models.ForeignKey(MeetingType)
    
    description = models.TextField(blank=True)
    prerequisites = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)    

    # instructors
    instructors = models.ManyToManyField(Instructor)

    # TAs
    teaching_assistants = models.ManyToManyField(TeachingAssistant, blank=True, null=True)
    
    # meeting date/time
    meeting_date = models.CharField(max_length=100)
    meeting_time = models.CharField(max_length=100)
    meeting_note = models.TextField(blank=True)    
    exam_group = models.CharField(max_length=20, blank=True)
    
    # room
    room = models.ForeignKey(Room)
    confirmation_status = models.ForeignKey(RoomStatus)

    # requirements
    mcb_required = models.BooleanField('Required for MCB')
    requirements_met = models.ManyToManyField(Requirement, blank=True, null=True)
    
    # enrollments
    enrollments_entered = models.BooleanField('Have the enrollments been entered?', default=False)
    undergrads_enrolled = models.IntegerField(default=0)
    grads_enrolled = models.IntegerField(default=0)
    employees_enrolled = models.IntegerField(default=0)
    cross_registered =  models.IntegerField(default=0)
    withdrawals = models.IntegerField(default=0)
    total_enrolled = models.IntegerField('total enrolled', help_text='auto-calculated', default=0)
    
    # budgets
    budget = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    budget_note = models.TextField(blank=True)
    
    # books 
    #books = models.ManyToManyField(Book, blank=True, null=True)
    #online_materials = models.ManyToManyField(OnlineMaterial)

    def save(self):
        self.total_enrolled = self.undergrads_enrolled + self.grads_enrolled + self.employees_enrolled 
        try:
            self.time_sort = datetime.date(self.year, self.term.sort_month, 1)
        except:
            self.time_sort = None
            
        super(SemesterDetails, self).save()


    #def department(self):
        #return self.course.department.abbreviation
    #    return self.course.course_id #department.abbreviation
    #department.allow_tags = True
    
    def budget_history(self):
        lst = SemesterDetails.objects.filter(course=self.course).order_by('-year', 'term')
        if lst.count() == 0:
            return '(no history)'
        return render_to_string('admin/course/semesterdetails/budget_history.html', { 'semester_details' : lst })      
    budget_history.allow_tags = True
    
    
    def enrollment_history(self):
          lst = SemesterDetails.objects.filter(course=self.course).order_by('-year', 'term')
          if lst.count() == 0:
              return '(no history)'
          return render_to_string('admin/course/semesterdetails/enrollment_history.html', { 'semester_details' : lst })
    enrollment_history.allow_tags = True
    
    def instructor_history(self):
          lst = SemesterDetails.objects.filter(course=self.course).order_by('-year', 'term')
          if lst.count() == 0:
              return '(no history)'
          return render_to_string('admin/course/semesterdetails/instructor_history.html', { 'semester_details' : lst })
    instructor_history.allow_tags = True
    
    
    def course_title(self):
        return self.course.title
        
    def instructors_list(self):
        lst = []
        for p in self.instructors.all():
            lst.append(p.fname_lname())
        return '<br />'.join(lst)
    instructors_list.allow_tags = True
    
    def __unicode__(self):
        return '%s - %s %s' % (self.course, self.year, self.term)

    class Meta:
        ordering = ('course', '-time_sort',) #'year', 'term',)
        verbose_name_plural = 'Semester details'
       
class SemesterInstructorQScore(models.Model):
    '''
    Record a Q score for a specific semester and instructor
    '''
    semester = models.ForeignKey(SemesterDetails)
    instructor = models.ForeignKey(Instructor)
    q_score = models.DecimalField(default=0, decimal_places=2, max_digits=9)

    #def save(self):
    class Meta:
        ordering = ('semester', 'instructor', )
        verbose_name = 'Semester Instructor Q Score'
        verbose_name_plural = 'Semester Instructor Q Scores'
        

    def __unicode__(self):
        return '%s, %s: %s' % (self.instructor, self.semester, self.q_score)


class SemesterInstructorCredit(models.Model):
    '''
    Record Credit for an instructor for this course
    '''
    semester = models.ForeignKey(SemesterDetails)
    instructor = models.ForeignKey(Instructor)
    credit_score = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    note = models.CharField(blank=True, max_length=255)

    class Meta:
        ordering = ('semester', 'instructor', )
        verbose_name = 'Semester Instructor Credit Score'
        verbose_name_plural = 'Semester Instructor Credit Scores'


    def __unicode__(self):
        return '%s, %s: %s' % (self.instructor, self.semester, self.credit_score)


class CourseDevelopmentCredit(models.Model):
    '''
    Record Credit for an instructor for this course
    '''
    semester = models.ForeignKey(SemesterDetails)
    instructor = models.ForeignKey(Instructor)
    course_development_credit = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    note = models.CharField(blank=True, max_length=255)

    class Meta:
        ordering = ('semester', 'instructor', )
        verbose_name = 'Course Development Credit Score'
        verbose_name_plural = 'Course Development Credit Scores'


    def __unicode__(self):
        return '%s, %s: %s' % (self.instructor, self.semester, self.course_development_credit)



from credit_score_maker import make_initial_semester_credit_entries
post_save.connect(make_initial_semester_credit_entries, sender=SemesterDetails)


    