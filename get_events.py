#!/usr/bin/env python3

# __author__ = "Eric Allen Youngson"
# __email__ = "eric@successionecological.com"
# __copyright__ = "Copyright 2015, Succession Ecological Services"
# __license__ = "GNU Affero (GPLv3)"

""" This module provides functions for requesting events from a Google
    Calendar account over a specified time period

    Starting point found @
https://developers.google.com/google-apps/calendar/quickstart/python """


from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
# from builtins import *
import os
import httplib2
from googleapiclient import discovery
import oauth2client
from oauth2client.file import Storage
from oauth2client import client, tools

from datetime import datetime, time, timedelta
from dateutil import parser
import parsedatetime
import pytz
from pytz import timezone
import calendar ##TODO(eayoungs@gmail.com): Remove when event_range() function
                #                           is revised

import pprint as pp


# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass


class NonConformantDateTime(Error):
   """Raised when the datetime object does not conform to expectations """
   pass


def _get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

    return credentials


def _create_svs_obj(credentials):
    """ Creates a Google Calendar API service object and outputs a list of the
        events on the user's calendar for a given period """

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    return service


def relative_datetime(relPeriod='today', tz='US/Pacific'):
    """ Takes a relative plain-text day and time zone, returns a datetime
        object corresponding to the colloquial date in the specified
        timezone """

    cal = parsedatetime.Calendar()
    datetimeObj, _ = cal.parseDT(datetimeString=relPeriod, tzinfo=timezone(tz))

    return datetimeObj


def midnight_datetime(dtime):
    """ Takes a datetime object and returns a datetime at midnight of the
        given day """

    midnightDt = dtime.replace(minute=0, hour=0, second=0, microsecond=0)

    return midnightDt


def iso_datetime(relRange):
    """  """

    (evStart, evEnd) = relRange
    isoPeriodBegin = evStart.isoformat()
    isoPeriodEnd = evEnd.isoformat()
    isoEvStart_isoEvEnd = (isoPeriodBegin, isoPeriodEnd)

    return isoEvStart_isoEvEnd


def relrange_today():
    """ Returns a StringType object containing a datetime object in ISO 8601
        format """

    periodBegin = midnight_datetime(relative_datetime('today'))
    periodEnd = periodBegin + timedelta(days=1)
    relToday = (periodBegin, periodEnd)

    return relToday


def relrange_thisweek():
    """  """

    periodBegin = midnight_datetime(relative_datetime('last saturday'))
    periodEnd = midnight_datetime(relative_datetime('sunday'))
    relWeek = (periodBegin, periodEnd)

    return relWeek


def relrange_thismonth():
    """  """

    thisDay = midnight_datetime(relative_datetime('today'))
    first_day_current = datetime(thisDay.year, thisDay.month, 1)
    periodBegin = thisDay.replace(day = 1)
    periodEnd = thisDay.replace(day = calendar.monthrange(thisDay.year,
                                                             thisDay.month)[1])
    relThisMonth = (periodBegin, periodEnd)

    return relThisMonth


def relrange_thisyear():
    """  """

    thisDay = midnight_datetime(relative_datetime('today'))
    periodEnd = datetime(thisDay.year, 12, 31)
    periodBegin = datetime(thisDay.year, 1, 1)
    relYear = (periodBegin, periodEnd)

    return relYear


def event_range(relRange='year', tz='US/Pacific'):
    """ Define the time range for the events to be selected from """

    #if begin=='none' and end=='none':
    # http://www.protocolostomy.com/2010/07/06/python-date-manipulation/
    datetimeObj = relative_datetime() # datetime.today()
    #today = datetimeObj.replace(tzinfo=None)
    # ParseDateTime: Today
    pdtToday = midnight_datetime(relative_datetime('today'))
    endOfToday = midnight_datetime(pdtToday) # today.replace(minute=0, hour=0, second=0, microsecond=0)
    if relRange == 'week':
        periodBegin = midnight_datetime(relative_datetime('last saturday'))
        periodEnd = midnight_datetime(relative_datetime('sunday'))
        # relDelta = endOfToday.isoweekday() + 1
        # periodBegin = endOfToday - timedelta(relDelta)
        # periodEnd = endOfToday - timedelta(relDelta-7)
    elif relRange == 'lastWeek':
        relDelta = endOfToday.isoweekday() + 1
        periodBegin = endOfToday - timedelta(relDelta+7)
        periodEnd = endOfToday - timedelta(relDelta)

    elif relRange == 'day': 
        periodBegin = pdtToday
        periodEnd = pdtToday + timedelta(days=1)
        # periodBegin = datetime.combine(today, time.min)
        # periodEnd = datetime.combine(today, time.max)
    elif relRange == 'yesterday':
        periodEnd= midnight_datetime(relative_datetime('today'))
        periodBegin= periodEnd- timedelta(days=1)
        # yesterday = today - timedelta(days=1)
        # periodBegin = datetime.combine(yesterday, time.min)
        # periodEnd = datetime.combine(yesterday, time.max)
    elif relRange == 'month':
        periodBegin = pdtToday.replace(day = 1)
        periodEnd = pdtToday.replace(
                day = calendar.monthrange(pdtToday.year, pdtToday.month)[1])
    elif relRange == 'lastMonth':
        periodBegin = pdtToday.replace(month = pdtToday.month - 1, day = 1)
        periodEnd = pdtToday.replace(
                   day = calendar.monthrange(pdtToday.year, pdtToday.month)[1])
    elif relRange == 'year':
        periodEnd = pdtToday.replace(month = 12, day = 31)
        periodBegin = pdtToday.replace(month = 1, day = 1)
    else:
        ## TODO: Add exception
        periodBegin = relRange[0]
        periodEnd = relRange[1]
    # else:
    #     periodBegin = parser.parse(begin)
    #     periodEnd = parser.parse(end)
 
    isoPeriodBegin = periodBegin.isoformat()# + tz
    isoPeriodEnd = periodEnd.isoformat()# + tz
    evStart_evEnd = (isoPeriodBegin, isoPeriodEnd)

    return evStart_evEnd

def get_events(service, evStart_evEnd, calendars):
    """ Creates a Google Calendar API service object and outputs a list of the
        events on the user's calendar for a given period """

    (evStart, evEnd) = evStart_evEnd
    eventsDct = {}
    for key, value in calendars.items():
        #print('Getting events for Production Calendar for : ', evStart)
        eventsResult = service.events().list(calendarId=value, timeMin=evStart,
                                             timeMax=evEnd, singleEvents=True,
                                             orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            print('No upcoming events found for: '+key)
        else:
            for event in events:
                event['start'] = event['start'].get('dateTime',
                                                    event['start'].get('date'))
                event['end'] = event['end'].get('dateTime',
                                                event['end'].get('date'))
            eventsDct[key] = events
    evStartEvEnd_eventsDct = (evStart_evEnd, eventsDct)

    return evStartEvEnd_eventsDct


if __name__ == '__main__':
    """  """ 

    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'LifeEnergy.io'

    credentials = _get_credentials() 
    service = _create_svs_obj(credentials)

    evStart_evEnd = event_range()
    calendars = {'Public':'successionecological.com_1hm3pcniuvqhdmb7o6ck2h6los@group.calendar.google.com'}
                #{'Sunrise and sunset for Portland':
                 #'i_71.63.230.104#sunrise@group.v.calendar.google.com'}
    evStartEvEnd_eventsDct = get_events(service, evStart_evEnd, calendars)
    (evStartEvEnd, eventsDct) = evStartEvEnd_eventsDct

    pp.pprint(eventsDct)
    pp.pprint(evStart_evEnd)
