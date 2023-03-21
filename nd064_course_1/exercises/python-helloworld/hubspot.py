

import requests
import json
from collections import defaultdict
from dateutil.parser import parse
import datetime

#print(json.dumps(json.loads(requests.get("https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=b3c7bc9cb298869fd9d694aa1923").text), indent=2))

def get_dataset():
  data = requests.get("https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=b3c7bc9cb298869fd9d694aa1923")
  return data.json()

# to append list of attendees per country basis
def addCountries(sessions, count, attendees, country_name, startDate):
    sessions.append(
        {
            'attendeeCount': count,
            'attendees': attendees if len(attendees)>0 else [],
            'name': country_name,
            'startDate': startDate if isinstance(startDate, str) else ""
        }
    )

def find_attendes(in_data):

  countries = defaultdict()
  sessions = []

  
  for person in in_data['partners']:

    # creat a mpping countrywise
    if person['country'] not in countries.keys():
      countries[person['country']] = defaultdict()

    # creat a mpping countrywise -> datewise
    for avlb in person['availableDates']:
      if avlb not in countries[person['country']]:
        countries[person['country']][avlb] = set()
      countries[person['country']][avlb].add(person['email'])

    
  for country, dates in countries.items():
    
    sorted_dates = sorted(dates.keys())
    attnedees_email = set()
    max_attendes = 0
    days = 0
    temp_date = datetime.datetime.today
    output = []

    for i in range(len(sorted_dates)-1):
      curr_date = sorted_dates[i]
      nxt_date = sorted_dates[i+1]
      current_date_formatted = parse(curr_date)
      current_tomorrow_formatted = parse(nxt_date)
      
      if current_tomorrow_formatted - current_date_formatted > datetime.timedelta(1):
        continue

      temp_attendees = dates[curr_date].intersection(dates[nxt_date])

      if len(temp_attendees) > max_attendes:
        max_attendes = len(temp_attendees)
        attnedees_email = list(temp_attendees)
        temp_date = curr_date

    addCountries(sessions, max_attendes, attnedees_email, country, temp_date)
    
  return {'countries': sessions}

def post_output(final_send):
    resp = requests.post('https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=b3c7bc9cb298869fd9d694aa1923', data=json.dumps(final_send))
    print(resp)

def main():
  in_data = get_dataset()
  #print(json.dumps(find_attendes(in_data), indent=2))
  output = find_attendes(in_data)
  post_output(output)

if __name__ == '__main__':
    main()
