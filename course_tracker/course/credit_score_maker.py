from course.models import SemesterDetails, SemesterInstructorCredit
from course_tracker.instructor.models import Instructor


def make_initial_semester_credit_entries(sender, **kwargs):
    """ sender is a SemesterDetails object"""
   
    semester = kwargs.get('instance', None)
    if semester is None:
        return
         
    # are there existing SemesterInstructorCredit objects?
    if SemesterInstructorCredit.objects.filter(semester=semester).count() > 0:
        # Initial SemesterInstructorCredit exist; exit out of there
        return
    
    for pi in semester.instructors.all():
        sic = SemesterInstructorCredit(semester=semester\
                , instructor=pi
                , credit_score=0
                , note='auto-added')
        sic.save()