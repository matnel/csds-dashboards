import collections
import datetime
from jinja2 import Template

from pyhy import people, courses

import argparse

parser = argparse.ArgumentParser(description="Produce teaching schedule for an organisational unit at University of Helsinki.")
parser.add_argument('organization_id', type=int, help='organization ID number')
parser.add_argument('--year', dest='year', type = int, default=courses._guess_study_year(), help='year of data production')
parser.add_argument('--output', dest='output', type = str, default='./', help='where output is stored')

args = parser.parse_args()

year = args.year

## people working in the organisation
staff = people.by_organisation( [ args.organization_id ] )

names = map( lambda person: person['firstnames'] + ' ' + person['lastname'], staff )
names = list( names )

staff_courses = {}

for name in names:
    for course in courses.search( name, academic_year = year ):
        staff_courses[ course['curId'] ] = course

staff_courses = staff_courses.values()

by_starting_time = collections.defaultdict( list )

for course in staff_courses:

    teachers = []
    for set in course['studyGroupSets']:
        for group in set['studySubGroups']:
            teachers += group['teacherNames']

    course['teachers'] = list( map( lambda x: x.replace('␟', '').strip() , teachers ) )

    course['clean_name'] = course['name']['en'] if 'en' in course['name'] else course['name']['fi']

    course['start_date'] = datetime.datetime.strptime( course['activityPeriod']['startDate'], '%Y-%m-%d' )
    course['end_date'] = datetime.datetime.strptime( course['activityPeriod']['endDate'], '%Y-%m-%d' )

    starting = course['start_date'].replace(day=1)

    by_starting_time[ starting ].append( course )


template = Template( open('courses_year.html').read() )
open( args.output + str( year ) + '.html', 'w').write( template.render( courses_by_start_month = by_starting_time ) )
