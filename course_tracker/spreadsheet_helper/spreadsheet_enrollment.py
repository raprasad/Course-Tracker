from django.db.models import Q
from django.template.defaultfilters import slugify
from django.db import connection

import datetime
import xlwt
from xlwt import easyxf
from common.msg_util import *
from common.xls_styles import *

from course.models import *
#from course.spreadsheet_maker import *



def get_instructor_name_lookup():
    lu = {}
    for t in Instructor.objects.all():
        lu.update({t.id: str(t)})
    return lu

def get_semester_to_instructor_lookup():
    # To stop from executing hundreds of queries, tie the semester id to the instructor names
    cursor = connection.cursor()
    cursor.execute("SELECT semesterdetails_id, instructor_id FROM course_semesterdetails_instructors;")
    
    lu_semester_to_instructor = {}  # { semester_id : [instructor_id, instructor_id, ...]}
    for r in cursor.fetchall(): 
        sid, iid = r
        instructor_ids = lu_semester_to_instructor.get(sid, [])
        instructor_ids.append(iid)
        lu_semester_to_instructor.update({ sid : instructor_ids})
    return lu_semester_to_instructor

def get_teacher_cell_info(course, teacher_lookup, semester_to_teacher_lookup):
    teachers = []
    for teacher_id in semester_to_teacher_lookup.get(course.id, None):
        if teacher_id is not None:
            teacher = teacher_lookup.get(teacher_id, None)
            if teacher is not None:
                teachers.append(teacher)
    if len(teachers) == 0:
        return '(not in database)'
        
    teachers.sort()
    return '\n'.join(teachers)
    

def make_enrollment_stats_spreadsheet(sheet1, info_line, courses, **kwargs):
    """Spreadsheet for MCB Core admin use"""
    if sheet1 is None:
        return None
    if courses is None:
        return sheet

    if info_line:
        sheet1.write(0, 0, info_line, style_info_cell)

    #   (header label, attribute, width)
    column_attributes = [ ('Year', 'year', 10)\
    ,('Term', 'term', 10)\
    ,('Time Sort', 'time_sort', 10)\
    ,('Instructors', 'instructor', 20)\
    ,('Course ID', 'course_id', 20)\
    ,('Course Title', 'course_title', 35)\
    ,('Undergrads Enrolled', 'undergrads_enrolled', 10)\
    ,('Grads Enrolled', 'grads_enrolled', 10)\
    ,('Employees Enrolled', 'employees_enrolled', 10)\
    ,('Cross Registered', 'cross_registered', 10)\
    ,('Withdrawals', 'withdrawals', 10)\
    ,('Total Enrollment', 'total_enrolled', 10)\
    ,('Notes', 'notes', 10)\
    ]

    #----------------------------
    # Add the header row and set column widths
    #----------------------------
    char_multiplier = 256
    excel_row_num = 1
    for col_idx, (col_name, attr_name, col_width) in enumerate(column_attributes):
        sheet1.write(excel_row_num, col_idx, col_name, style_header)
        sheet1.col(col_idx).width = col_width * char_multiplier  

    teacher_lookup = get_instructor_name_lookup()
    semester_to_teacher_lookup = get_semester_to_instructor_lookup()
    
    NOT_FOUND = 'NOT_FOUND'
    
    # Iterate through each course 
    for course in courses:
        excel_row_num+=1
        
        for col_idx, (col_name, attr, col_width) in enumerate(column_attributes):
            if attr in ['notes']:
                sheet1.write(excel_row_num, col_idx, '', style_info_cell_wrap_on)
            elif attr == 'instructor':
                teacher_names = get_teacher_cell_info(course, teacher_lookup, semester_to_teacher_lookup)
                sheet1.write(excel_row_num, col_idx, teacher_names, style_info_cell_wrap_on)
            elif attr == 'term':
                sheet1.write(excel_row_num, col_idx, course.term.name, style_info_cell_wrap_on)
            elif attr == 'course_id':
                sheet1.write(excel_row_num, col_idx, course.course.course_id, style_info_cell_wrap_on)
            elif attr == 'course_title':
                sheet1.write(excel_row_num, col_idx, course.course.title, style_info_cell_wrap_on)    
            elif attr in [ 'undergrads_enrolled', 'grads_enrolled','employees_enrolled', 'cross_registered',  'withdrawals',  'total_enrolled']:
                sheet1.write(excel_row_num, col_idx, course.__dict__.get(attr,  ''), style_info_cell_wrap_on)                  
            else:
                sheet1.write(excel_row_num, col_idx, unicode(course.__dict__.get(attr,  '')), style_info_cell_wrap_on)  
        
    return sheet1



