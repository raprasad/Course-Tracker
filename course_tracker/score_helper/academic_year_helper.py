
# determine the academic year based on 'year' and 'CourseTerm'

def get_academic_year(course_term, year):
    if course_term is None or year is None or course_term.__dict__.get('sort_month', None) is None:
        return None
    
    if course_term.sort_month >= 8:     # Fall
        return '%s / %s' % (year, year+1)
    elif course_term.sort_month < 8:    # Spring
        return '%s / %s' % (year-1, year)
        
    return '(academic year?)'