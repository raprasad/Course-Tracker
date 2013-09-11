from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from course.models import *
from spreadsheet_helper.spreadsheet_maker import make_course_roster
from spreadsheet_helper.spreadsheet_enrollment import make_enrollment_stats_spreadsheet

import datetime
import xlwt

def view_course_enrollments(request):
    if not (request.user.is_authenticated() and request.user.is_staff):  
        return HttpResponse('not accessible')
    
    courses = SemesterDetails.objects.all().select_related().order_by('time_sort')

    if courses.count() == 0:
        return HttpResponse('Sorry!  No courses found.  Please click the "back" button on your browser')
        
    book = xlwt.Workbook(encoding="utf-8")
    # With a workbook object made we can now add some sheets.
    sheet1 = book.add_sheet('LSDIV courses')

    date_obj = datetime.datetime.now()
    info_line = "Generated on %s" % (date_obj.strftime('%m/%d/%Y - %I:%M %p'))

    sheet1 = make_course_roster(sheet1, info_line, courses)

    fname = 'lsdiv_enrollment_%s.xls' % (date_obj.strftime('%m%d-%I-%M%p-%S').lower())
    
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % (fname)

    # send .xls spreadsheet to response stream
    book.save(response)
    
    # for debugging
    # note: extra queries are from projecting 2012 enrollments
    #return render_to_response('sql_query_debug.html', {}, context_instance=RequestContext(request))

    return response

def view_below_300_course_enrollments(request):
    if not (request.user.is_authenticated() and request.user.is_staff):  
        return HttpResponse('not accessible')

    courses = SemesterDetails.objects.select_related('course', 'term', 'instructors').filter(course__course_sort_number__lte=300).order_by('-time_sort', 'course__course_sort_field')

    if courses.count() == 0:
     return HttpResponse('Sorry!  No courses found.  Please click the "back" button on your browser')

    book = xlwt.Workbook(encoding="utf-8")
    # With a workbook object made we can now add some sheets.
    sheet1 = book.add_sheet('Below 300-level')

    date_obj = datetime.datetime.now()
    info_line = "Generated on %s" % (date_obj.strftime('%m/%d/%Y - %I:%M %p'))

    sheet1 = make_enrollment_stats_spreadsheet(sheet1, info_line, courses)

    fname = 'below_300_course_enrollment_%s.xls' % (date_obj.strftime('%m%d-%I-%M%p-%S').lower())

    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % (fname)

    book.save(response)

    return response

def view_all_course_enrollments(request):
    if not (request.user.is_authenticated() and request.user.is_staff):  
        return HttpResponse('not accessible')

    courses = SemesterDetails.objects.select_related('course', 'term', 'instructors').all().order_by('-time_sort', 'course__course_sort_field')

    if courses.count() == 0:
     return HttpResponse('Sorry!  No courses found.  Please click the "back" button on your browser')

    book = xlwt.Workbook(encoding="utf-8")
    # With a workbook object made we can now add some sheets.
    sheet1 = book.add_sheet('courses')

    date_obj = datetime.datetime.now()
    info_line = "Generated on %s" % (date_obj.strftime('%m/%d/%Y - %I:%M %p'))

    sheet1 = make_enrollment_stats_spreadsheet(sheet1, info_line, courses)

    fname = 'all_course_enrollment_%s.xls' % (date_obj.strftime('%m%d-%I-%M%p-%S').lower())

    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % (fname)

    book.save(response)

    return response

    
    
    
def view_mcb_related_course_enrollments(request):
    """Quick report for catherine -- should later be made into gui where you select depts to filter"""
    if not (request.user.is_authenticated() and request.user.is_staff):  
        return HttpResponse('not accessible')

    depts = { 'MCB' : 'Molecular and Cellular Biology'\
            , 'NEUROBIO' : 'Neurobiology FAS'\
            , 'CPB' : 'Chemical and Physical Biology'\
            , 'LS' : 'Life Sciences'\
            , 'LPS' : 'Life and Physical Sciences'\
             }
            
    selected_departments = Department.objects.filter(abbreviation__in=depts.keys())
    dept_courses = Course.objects.filter(department__in=selected_departments)
    courses = SemesterDetails.objects.select_related(\
                            'course', 'term', 'instructors'\
                            ).filter(course__in=dept_courses\
                            ).order_by('-time_sort', 'course__course_sort_field')

    if courses.count() == 0:
        return HttpResponse('Sorry!  No courses found.  Please click the "back" button on your browser')

    book = xlwt.Workbook(encoding="utf-8")
    # With a workbook object made we can now add some sheets.
    sheet1 = book.add_sheet('MCB-related courses')

    date_obj = datetime.datetime.now()
    info_line = "Generated on %s" % (date_obj.strftime('%m/%d/%Y - %I:%M %p'))

    sheet1 = make_enrollment_stats_spreadsheet(sheet1, info_line, courses)

    fname = 'mcb-related_enrollment_%s.xls' % (date_obj.strftime('%m%d-%I-%M%p-%S').lower())

    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s' % (fname)

    # send .xls spreadsheet to response stream
    book.save(response)

    # for debugging
    # note: extra queries are from projecting 2012 enrollments
    #return render_to_response('sql_query_debug.html', {}, context_instance=RequestContext(request))

    return response

