from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from course.models import *
from course.spreadsheet_maker import make_course_roster
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
       