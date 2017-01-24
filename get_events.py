#!/usr/bin/env python3

# __author__ = "Eric Allen Youngson"
# __email__ = "eric@successionecological.com"
# __copyright__ = "Copyright 2015, Succession Ecological Services"
# __license__ = "GNU Affero (GPLv3)"

""" This module provides functions for requesting events from a Google
    Calendar account over a specified time period """


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
import calendar
import csv

import parsedatetime
import pytz
from pytz import timezone

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'LifeEnergy.io'


def get_credentials():
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


def create_svs_obj(credentials):
    """ Creates a Google Calendar API service object and outputs a list of the
        events on the user's calendar for a given period """

    # TODO (eayoungs): Move project from httplib2 to requests!
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    return service


def relative_datetime(relPeriod='today', tz='US/Pacific'):
    """ Takes a relative plain-text day and time zone, returns a datetime
        object corresponding to the colloquial date in the specified
        timezone """

    cal = parsedatetime.Calendar()
    datetimeObj, _ = cal.parseDT(datetimeString=relPeriod, tzinfo=timezone(
                                  tz))

    return datetimeObj


def midnight_datetime(dtime):
    """ Takes a datetime object and returns a datetime at midnight of the
        given day """

    midnightDt = dtime.replace(minute=0, hour=0, second=0, microsecond=0)

    return midnightDt


def event_range(relRange='week', tz='z'):
    """ Define the time range for the events to be selected from """

    #if begin=='none' and end=='none':
    # http://www.protocolostomy.com/2010/07/06/python-date-manipulation/
    datetimeObj = relative_datetime() # datetime.today()
    today = datetimeObj.replace(tzinfo=None)
    endOfToday = midnight_datetime(today) # today.replace(minute=0, hour=0, second=0, microsecond=0)
    if relRange == 'week':
        periodBegin = midnight_datetime(relative_datetime(
                                         'last saturday')).replace(tzinfo=None)
        periodEnd = midnight_datetime(relative_datetime(
                                         'saturday')).replace(tzinfo=None)
        # relDelta = endOfToday.isoweekday() + 1
        # periodBegin = endOfToday - timedelta(relDelta)
        # periodEnd = endOfToday - timedelta(relDelta-7)
    elif relRange == 'lastWeek':
        relDelta = endOfToday.isoweekday() + 1
        periodBegin = endOfToday - timedelta(relDelta+7)
        periodEnd = endOfToday - timedelta(relDelta)
    elif relRange == 'day':
        periodBegin = midnight_datetime(relative_datetime(
                                         'yesterday')).replace(tzinfo=None)
        periodEnd = midnight_datetime(relative_datetime(
                                         'today')).replace(tzinfo=None)
        # periodBegin = datetime.combine(today, time.min)
        # periodEnd = datetime.combine(today, time.max)
    elif relRange == 'yesterday':
        yesterday = today - timedelta(days=1)
        periodBegin = datetime.combine(yesterday, time.min)
        periodEnd = datetime.combine(yesterday, time.max)
    elif relRange == 'month':
        first_day_current = datetime(today.year, today.month, 1)
        periodBegin = today.replace(day = 1)
        periodEnd = today.replace(
                     day = calendar.monthrange(today.year, today.month)[1])
    elif relRange == 'lastMonth':
        first_day_current = datetime(today.year, today.month, 1)
        last_day_previous = first_day_current - timedelta(days=1)
        first_day_previous = datetime(
                        last_day_previous.year, last_day_previous.month, 1)
        periodBegin = first_day_previous 
        periodEnd = last_day_previous
    elif relRange == 'year':
        periodBegin = datetime(today.year, 1, 1)
        periodEnd = datetime(today.year, 12, 31)
    else:
        ## TODO: Add exception
        periodBegin = relRange[0]
        periodEnd = relRange[1]
    # else:
    #     periodBegin = parser.parse(begin)
    #     periodEnd = parser.parse(end)
 
    isoPeriodBegin = periodBegin.isoformat() + tz
    isoPeriodEnd = periodEnd.isoformat() + tz
    evStart_evEnd = (isoPeriodBegin, isoPeriodEnd)

    return evStart_evEnd

def get_events(service, evStart_evEnd, calendars):
    """ Creates a Google Calendar API service object and outputs a list of the
        events on the user's calendar for a given period """

    (evStart, evEnd) = evStart_evEnd
    eventsDct = {}
    for calendar in calendars:
        #print('Getting events for Production Calendar for : ', evStart)
        eventsResult = service.events().list(calendarId=calendar,
                                             timeMin=evStart,
                                             timeMax=evEnd, singleEvents=True,
                                             orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        # TODO: Store empty calendars for reporting?
        # if not events:
        #     print('No upcoming events found for: '+key)
        # else:
        for event in events:
            event['start'] = event['start'].get('dateTime',
                                                event['start'].get('date'))
            event['end'] = event['end'].get('dateTime',
                                            event['end'].get('date'))
        eventsDct[calendar] = events
    evStartEvEnd_eventsDct = (evStart_evEnd, eventsDct)

    return evStartEvEnd_eventsDct
