from django.db.models import Q
from django.template.defaultfilters import slugify
import datetime
import xlwt
from xlwt import easyxf
from common.msg_util import *
from common.xls_styles import *

from course.models import *
from course.spreadsheet_maker import *

'''
python manage.py shell
from course.spreadsheet_maker import *
make_course_excel_file()

        
'''

def make_course_excel_file():
    """From the Django admin view of a Person->Lab object, generate an Excel spreadsheet"""

    courses = SemesterDetails.objects.all().order_by('time_sort')

    if courses.count() == 0:
        return 
        msgx('Sorry!  No courses found!')
    
    book = xlwt.Workbook(encoding="utf-8")
    # With a workbook object made we can now add some sheets.
    sheet1 = book.add_sheet('LSDIV courses')

    date_obj = datetime.datetime.now()
    info_line = "Generated on %s" % (date_obj.strftime('%m/%d/%Y - %I:%M %p'))

    sheet1 = make_course_roster(sheet1, info_line, courses)

    # create response object
    fname = 'lsdiv_enrollment_%s.xls' % (date_obj.strftime('%m%d-%I-%M%p-%S').lower())
    #fname = os.path.join(CANDIDATE_FINAL_DOCS, fname)
    
    # send .xls spreadsheet to response stream
    book.save(fname)
    msg('xls created: %s' % fname)
    
    os.system('open %s' % fname)
    
def get_projected_enrollment(semester):
    
    for sd in SemesterDetails.objects.exclude(id=semester.id).exclude(year=2012).filter(course=semester.course).order_by('-time_sort'):
        return sd
    return None
    
def make_course_roster(sheet1, info_line, courses, **kwargs):
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
    ,('Instructor', 'instructor', 20)\
    ,('Course ID', 'course_id', 20)\
    ,('Course Title', 'course_title', 35)\
    ,('Total Enrollment', 'total_enrolled', 10)\
    ,('2012 Projected Enrollment', 'projected', 10)\
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

    for course in courses:
        #msgt('process: %s' % course)
        for teacher in course.instructors.all():
            #msg('instructor: %s' % teacher)
            excel_row_num +=1
            
            for col_idx, (col_name, attr, col_width) in enumerate(column_attributes):
                if attr in ['notes']:
                    continue
                elif attr == 'instructor':
                    sheet1.write(excel_row_num, col_idx, unicode(teacher), style_info_cell_wrap_on)
                elif attr == 'term':
                    sheet1.write(excel_row_num, col_idx, course.term.name, style_info_cell_wrap_on)
                elif attr == 'course_id':
                    sheet1.write(excel_row_num, col_idx, course.course.course_id, style_info_cell_wrap_on)
                elif attr == 'course_title':
                    sheet1.write(excel_row_num, col_idx, course.course.title, style_info_cell_wrap_on)
                elif attr == 'projected':
                    if not course.year == 2012:
                        sheet1.write(excel_row_num, col_idx, '(n/a)', style_info_cell_wrap_on)
                        col_idx+=1
                        sheet1.write(excel_row_num, col_idx, '', style_info_cell_wrap_on)
                        continue
                    
                    last_semester = get_projected_enrollment(course)
                    if last_semester is None:
                        sheet1.write(excel_row_num, col_idx, '(n/a)', style_info_cell_wrap_on)
                        col_idx+=1
                        sheet1.write(excel_row_num, col_idx, 'new course)', style_info_cell_wrap_on)                        
                    else:
                        sheet1.write(excel_row_num, col_idx, str(last_semester.total_enrolled), style_info_cell_wrap_on)
                        col_idx+=1
                        sheet1.write(excel_row_num, col_idx, 'based on %s %s' % (last_semester.term, last_semester.year), style_info_cell_wrap_on)                        
                elif attr == 'course_title':
                        sheet1.write(excel_row_num, col_idx, str(course.total_enrolled), style_info_cell_wrap_on)

                else:
                    sheet1.write(excel_row_num, col_idx, unicode(course.__dict__.get(attr,  '')), style_info_cell_wrap_on)  
            col_idx+=1

    return sheet1



