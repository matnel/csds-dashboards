import collections
import datetime

from pyhy import people, courses


## people working in CSDS
staff = people.by_organisation( [62060775] )

names = map( lambda person: person['firstnames'] + ' ' + person['lastname'], staff )
names = list( names )

print( names )
staff_courses = {}

for name in names:
    for course in courses.search( name, academic_year = 2018 ):
        staff_courses[ course['curId'] ] = course

staff_courses = staff_courses.values()

by_starting_time = collections.defaultdict( list )

for course in staff_courses:

    teachers = []
    print( course )
    print( course.keys() )
    for set in course['studyGroupSets']:
        for group in set['studySubGroups']:
            teachers += group['teacherNames']

    course['teachers'] = list( map( lambda x: x.replace('␟', '').strip() , teachers ) )

    course['clean_name'] = course['name']['en'] if 'en' in course['name'] else course['name']['fi']

    course['start_date'] = datetime.datetime.strptime( course['activityPeriod']['startDate'], '%Y-%m-%d' )
    course['end_date'] = datetime.datetime.strptime( course['activityPeriod']['endDate'], '%Y-%m-%d' )

    starting = course['start_date'].replace(day=1)

    by_starting_time[ starting ].append( course )

from jinja2 import Template

template = Template( open('courses_year.html').read() )
open('2018.html', 'w').write( template.render( courses_by_start_month = by_starting_time ) )
