from django.db.models import Q

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer

from course_tracker.course_parameters.models import CourseStatus
from course.models import Course, SemesterDetails
from department.models import Department
from instructor.models import Instructor
    
"""
class CourseSemesterInfo:
    def __init__(self, course_id):
        try:
            self.course = SemesterDetails.objects.get(id=person_id)
        except Person.DoesNotExist:
            self.person = None
            
        if self.person:
            self.load_additional_info()
    
    def load_titles(self):
        if self.person.title:
            self.titles= [self.person.title.title]
            for title in self.person.get_secondary_titles():
                self.titles.append(title.title)
        else:
            self.titles = None
            
    def load_additional_info(self):
        self.load_titles() 
        self.load_faculty_info()
        
    def load_faculty_info(self):
        self.research_summary = None
        self.rank = None
        try:
            faculty_member = self.person.facultymember
            self.research_summary = faculty_member.research_summary
            if faculty_member.category:
                self.rank = faculty_member.category.name
        except FacultyMember.DoesNotExist:
            pass
    
    def get_building_name(self):
        if self.person and self.person.building:
            return self.person.building.name
        return None
        
    def get_dict(self):
        return { 'titles' : self.titles
                , 'room' : self.person.room
                , 'building' : self.get_building_name()
                , 'appointment' : self.person.appointment.name
                , 'dept_abbreviation' : self.person.affiliation
                , 'research_interest' : self.research_summary
                , 'rank' : self.rank
                
                }
"""

class MCBCourseFilter:
    """
    Choose courses that are:
        (1) active and bracketed
        (2) MCB courses or are taught my MCB faculty 
        (3) NOT 300 level
    """
    @staticmethod
    def get_valid_statuses():
        return CourseStatus.objects.filter(Q(name__icontains='active')\
                                        | Q(name__icontains='bracketed')).values_list('id', flat=True)
    
    @staticmethod
    def get_mcb_department():
        return Department.objects.filter(abbreviation='MCB')  
    
    @staticmethod
    def get_mcb_faculty():
        dept_mcb = MCBCourseFilter.get_mcb_department()
        return Instructor.objects.filter(Q(primary_affiliation=dept_mcb)\
                                        | Q(other_affiliations=dept_mcb))
    
    @staticmethod
    def get_semester_details():
        
        # valid course statuses: active and bracketd
        valid_statuses = MCBCourseFilter.get_valid_statuses()
        
        # mcb department
        dept_mcb = MCBCourseFilter.get_mcb_department()
        
        # mcb faculty
        mcb_faculty = MCBCourseFilter.get_mcb_faculty()
    
        # ids of courses taught by MCB faculty
        queryset = SemesterDetails.objects.filter(course__status__id__in=valid_statuses).filter(Q(instructors__in=mcb_faculty) \
                            | Q(course__department=dept_mcb) )
        
        # Exclude 300 level courses
        queryset = queryset.exclude(course__course_id__regex='3\d\d')
        
        return queryset
    
    @staticmethod
    def get_mcb_courses():
        
        semester_detail_ids = MCBCourseFilter.get_semester_details().values_list('course__id', flat=True)
        
        #  Valid MCB courses and courses taught by MCB faculty
        queryset = Course.objects.filter(id__in=semester_detail_ids)
        
        # Exclude 300 level courses
        queryset = queryset.exclude(course_id__regex='3\d\d')
        
        return queryset

class SemesterDetailsResource(ModelResource):
    # http://127.0.0.1:8000/course-tracker/mcb-api/directory/v1/person/1238/?format=json
    #def dehydrate(self, bundle):
    #    cs_info = CourseSemesterInfo(bundle.data.get('id'))
    #    bundle.data.update(cs_info.get_dict())
    #    return bundle

    class Meta:

        queryset = MCBCourseFilter.get_semester_details()
        resource_name = 'semester'


class CourseResource(ModelResource):
    # http://127.0.0.1:8000/course-tracker/mcb-api/directory/v1/person/1238/?format=json
    #def dehydrate(self, bundle):
    #    cs_info = CourseSemesterInfo(bundle.data.get('id'))
    #    bundle.data.update(cs_info.get_dict())
    #    return bundle
        
    class Meta:

        queryset = MCBCourseFilter.get_mcb_courses()
        resource_name = 'course'
        
        
"""

t = Course.objects.filter(course_id__regex=r'^(3{\d2}) +')
"""
