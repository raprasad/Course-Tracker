from course.models import *
from course.spreadsheet_maker import *


def view_course_enrollments(request):
    if not (request.user.is_authenticated() and request.user.is_staff):  
        return HttpResponse('not accessible')
    
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=lab_%s_%s.xls' % (lab.url, date_obj.strftime('%m%d-%I-%M%p-%S').lower())

    # send .xls spreadsheet to response stream
    book.save(response)
    return response