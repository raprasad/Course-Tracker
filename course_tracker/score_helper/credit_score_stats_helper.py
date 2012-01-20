from decimal import Decimal
from score_helper.academic_year_helper import get_academic_year
"""
Quick class for summing credit scores, finding avg, mean, etc.
"""

class AcademicYearSummary:
    def __init__(self, academic_year):
        self.academic_year = academic_year
        self.semester_credit_objects = []        # SemesterInstructorCredit objects
        self.course_dev_credit_objects = []  # CourseDevelopmentCredit objects
        self.academic_credit_objects = []    # AcademicYearCredit objects
         
        self.semester_score_total = 0
        self.course_dev_score_total = 0
        self.academic_score_total = 0
        self.grand_total_score = 0
        
        
    def calc_academic_year_scores(self):
        if len(self.semester_credit_objects) > 0:
            self.semester_score_total = sum(map(lambda x: x.credit_score, self.semester_credit_objects))

        if len(self.course_dev_credit_objects) > 0:
            self.course_dev_score_total = sum(map(lambda x: x.course_development_credit, self.course_dev_credit_objects))

        if len(self.academic_credit_objects) > 0:
            self.academic_score_total = sum(map(lambda x: x.credit_score, self.academic_credit_objects))
        
        self.grand_total_score = self.semester_score_total + self.course_dev_score_total  + self.academic_score_total
        
class CreditScoreStatsHelper:
    """Simple calculation results used to display credit history information in a template.
    Instructors have 3 types of credit scores:
        (a) teaching
        (b) course development
        (c) academic, e.g. head tutor, department chair, etc.
        
    Steps
        (a) Organize all scores 
    """
    
    def __init__(self, instructor, exclude_zero_scores=True):
            
        self.semester_credit_score_history = instructor.semesterinstructorcredit_set.all()
        self.course_development_history = instructor.coursedevelopmentcredit_set.all()
        self.academic_credit_history = instructor.academicyearcredit_set.all()
        
        if exclude_zero_scores:
            self.semester_credit_score_history = filter(lambda x: x.credit_score > 0, self.semester_credit_score_history)
        
        # make a list of credit scores to use for mean/median
        self.credit_score_list = map(lambda x: x.credit_score, self.semester_credit_score_history)
        
        # semester credit score variables
        self.sum_score = Decimal('0')
        self.mean_score = Decimal('0')
        self.median_score = Decimal('0')
        self.num_scores = 0    

        # development score variables
        self.sum_development_score = Decimal('0')
        self.num_development_scores = 0

        # academic score variables
        self.sum_academic_score = Decimal('0')
        self.num_academic_scores = 0

        self.grand_total_score = 0

        
        # make calculations
        self.calc_semester_credit_scores()
        self.calc_development_scores()
        self.calc_academic_scores()
        self.calc_grand_total()
        
        # summary by academic year
        self.academic_year_summary_lu = {}
        self.create_academic_year_summaries()
    
    def calc_grand_total(self):
        self.grand_total_score = self.sum_score + self.sum_development_score +self.sum_academic_score
        
    def get_academic_year_summary_count(self):
        if self.academic_year_summary_lu is None:
            return 0
        return len(self.academic_year_summary_lu)
    
    def get_academic_year_summaries(self):
        summaries = self.academic_year_summary_lu.values()
        summaries.sort(key=lambda x: x.academic_year)
    
        #for summ in summaries:
        #    print summ
        #print '-' *40
        return summaries
        
    def create_academic_year_summaries(self):
        self.academic_year_summary_lu = {}
        
        # separate semester scores by academic year
        for obj in self.semester_credit_score_history:
            academic_year = get_academic_year(obj.semester.term, obj.semester.year)
            academic_year_summary = self.academic_year_summary_lu.get(academic_year, AcademicYearSummary(academic_year))
            academic_year_summary.semester_credit_objects.append(obj)
            self.academic_year_summary_lu.update({ academic_year:academic_year_summary })   
        
        # separate course dev. scores by academic year
        for obj in self.course_development_history:
            academic_year = get_academic_year(obj.semester.term, obj.semester.year)
            academic_year_summary = self.academic_year_summary_lu.get(academic_year, AcademicYearSummary(academic_year))
            academic_year_summary.course_dev_credit_objects.append(obj)
            self.academic_year_summary_lu.update({ academic_year:academic_year_summary })   
        
        # separate academic scores by academic year
        for obj_academic_yr in self.academic_credit_history:
            academic_year = get_academic_year(obj_academic_yr.term, obj_academic_yr.year)
            academic_year_summary = self.academic_year_summary_lu.get(academic_year, AcademicYearSummary(academic_year))
            academic_year_summary.academic_credit_objects.append(obj_academic_yr)
            self.academic_year_summary_lu.update({ academic_year:academic_year_summary })   

        
        for academic_year_summary in self.academic_year_summary_lu.values():
            academic_year_summary.calc_academic_year_scores()
        
    def calc_academic_scores(self):
        dev_scores = map(lambda x: x.credit_score, self.academic_credit_history)
        self.sum_academic_score = sum(dev_scores)
        self.num_academic_scores = len(dev_scores)

    
    def calc_development_scores(self):
        dev_scores = map(lambda x: x.course_development_credit, self.course_development_history)
        self.sum_development_score = sum(dev_scores)
        self.num_development_scores = len(dev_scores)
        
    def calc_semester_credit_scores(self):
        if self.credit_score_list is None or len(self.credit_score_list) == 0:
            return
            
        self.credit_score_list.sort()   # sort to help find median
        self.sum_score = sum(self.credit_score_list)

        self.num_scores = len(self.credit_score_list)
        if self.num_scores == 0:
            return
            
        self.mean_score = self.sum_score / self.num_scores
        
        if len(self.credit_score_list) == 1:
            self.median_score = self.credit_score_list[0]
        
        elif len(self.credit_score_list) % 2 == 1:   # odd number, take middle score
            self.median_score = self.credit_score_list[self.num_scores/2]
        
        else:   # even number, avg middle two numbers
            mid_right  = self.credit_score_list[ self.num_scores/2 ]
            mid_left = self.credit_score_list[ (self.num_scores/2)-1 ]
            self.median_score = (mid_left + mid_right) / Decimal('2')
        
        
        
