#!/usr/bin/env python

""" This module creates a webisite using the Flask webframework and the Google
    API implementation of the OAuth 2.0 authentication protocol to allow the
    app to parse your Google Calendars. It also uses a library, written by the
    same author, to provide summary statistics about your events. """

__author__ = "Eric Allen Youngson"
__email__ = "eayoungs@gmail.com"
__copyright__ = "Copyright 2017 Eric Youngson"
__license__ = "Apache 2.0"

import os
import json
import re
import uuid
import httplib2

from flask import (Flask, render_template, session, redirect, url_for, request,
                   send_file)
# from bootstrap_flask import create_app
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from googleapiclient import discovery

from forms import CalendarSelectForm
from geepal import get_events as ge
from geepal import dfsort as dfs
import invoice


app = Flask(__name__)  # app = create_app()
app.secret_key = str(uuid.uuid4())
app.config.from_pyfile('settings.cfg')
BASE_URL = app.config['BASE_URL']
CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']
SCOPE = app.config['SCOPE']
REDIRECT_URI = app.config['REDIRECT_URI']


@app.route('/')
def main():
    os.system('rm ./invoice.pdf')
    return render_template('template.html',
                           homeBttnClass="active",
                           homeUrl=BASE_URL,
                           aboutUrl=BASE_URL+"about",
                           contactUrl=BASE_URL+"contact",
                           quoteText='Everything',
                           quoteAttrib='"This Moment is All there Is" --Rumi',
                           subheading1='Build your routine, your way',
                           subtext1=''' Find out where your spend your time,
                                        setgoals and check in on your progress
                                        with minimal effort--all in from within
                                        the calendar you already know & love:
                                        Google Calendar''',
                           subheading2="Show the muse you're serious",
                           subtext2=''' You have to show up for your dreams; on
                                        one can do it for you but we can give
                                        you the tools to stay present''',
                           appBttnUrl=BASE_URL+"google_oauth2")


@app.route('/downloads')
def return_file():
    return send_file('invoice.pdf')


@app.route('/google_oauth2', methods=['GET', 'POST'])
def google_oauth2():
    if 'credentials' not in session:
        return redirect(url_for('callback'))
    # Why is this not indented?
    credentials = OAuth2Credentials.from_json(session['credentials'])

    if credentials.access_token_expired:
        return redirect(url_for('callback'))

    else:
        form = CalendarSelectForm()
        # https://developers.google.com/api-client-library/python/auth/web-app

        http_auth = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http_auth)
        # https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list#try-it
        page_token = None
        while True:
            calendar_list = service.calendarList().list(
                                                pageToken=page_token).execute()
            calendarsDct = {}
            for calendar_list_entry in calendar_list['items']:
                # Object creation order seems to be reversed:
                # just going with it here...¯\_(ツ)_/¯ (see ln91)
                calendarsDct[
                    calendar_list_entry['id']] = calendar_list_entry['summary']
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        form.Calendars.choices = calendarsDct.items()

        if request.method == 'POST':
            if form.validate() is False:
                return render_template('forms_template.html', form=form,
                                       homeBttnClass="active",
                                       homeUrl=BASE_URL,
                                       aboutUrl=BASE_URL+"about",
                                       contactUrl=BASE_URL+"contact",
                                       quoteAttrib='''Congratulations; you've
                                                      authorized Timing.Is to
                                                      access your Google
                                                      Calendar data! To revoke
                                                      authorization visit your
                                                      Google account @ ''',
                                       link='''
                                   https://myaccount.google.com/permissions''',
                                       linktext='''
                                   https://myaccount.google.com/permissions''',
                                       )
            else:  # Reverse logical order of dicitonary (see ln73)
                try:
                    calendarsSelectedDct = {value: key
                                            for key, value
                                            in form.Calendars.choices
                                            if key
                                            in form.Calendars.data
                                            }
                    evStart_evEnd = ge.event_range(
                        relRange=form.DateRange.data)
                    evStartEvEnd_eventsDct = ge.get_events(
                        service, evStart_evEnd, calendarsSelectedDct)
                    # TODO: Test for empty dict (no events)
                    (evStart_evEnd, eventsDct) = evStartEvEnd_eventsDct
                    evStartEvEnd_calEvDfsDct = dfs.add_durations(
                                                        evStartEvEnd_eventsDct)
                except Exception as e:
                    print(e)

                for key, value in calendarsSelectedDct.items():
                    try:
                        eventTypesDct = dfs.get_unique_events(
                                                      evStartEvEnd_calEvDfsDct,
                                                      key)
                        if form.Tag.data:
                            invoiceItemsDct = dfs.invoice_dict(eventTypesDct,
                                                               form.Tag.data)
                        else:
                            invoiceItemsDct = dfs.invoice_dict(eventTypesDct)
                    except Exception as e:
                        print(e)
                        return render_template('forms_template.html',
                                               form=form,
                                               homeBttnClass="active",
                                               homeUrl=BASE_URL,
                                               aboutUrl=BASE_URL+"about",
                                               contactUrl=BASE_URL+"contact",
                                               quoteAttrib='''Congratulations;
                                                    you've authorized Timing.Is
                                                    to access your Google
                                                    Calendar data! To revoke
                                                    authorization visit your
                                                    Google account @ ''',
                                               link='''
                                   https://myaccount.google.com/permissions''',
                                               linktext='''
                                   https://myaccount.google.com/permissions''',
                                               )

                    if form.billing_rate.data:
                        billing_rate = form.billing_rate.data
                    else:
                        billing_rate = '1'
                    if form.provider_tax_rate.data:
                        provider_tax_rate = form.provider_tax_rate.data
                    else:
                        provider_tax_rate = 0
                    if form.invoice_id.data:
                        invoice_id = form.invoice_id.data
                    else:
                        invoice_id = 1
                    invoice.main(invoiceItemsDct,
                                 billing_rate=billing_rate,
                                 provider_email=form.provider_email.data,
                                 client_email=form.client_email.data,
                                 provider_name=form.provider_name.data,
                                 provider_street=form.provider_street.data,
                                 provider_city=form.provider_city.data,
                                 provider_state=form.provider_state.data,
                                 provider_country=form.provider_country.data,
                                 provider_post_code=form.provider_post_code.data,
                                 provider_tax_rate=provider_tax_rate,
                                 invoice_id=invoice_id
                                 )

                try:
                    return redirect(url_for('return_file'))
                except Exception as e:
                    print(e)
                    return render_template('forms_template.html', form=form,
                                           homeBttnClass="active",
                                           homeUrl=BASE_URL,
                                           aboutUrl=BASE_URL+"about",
                                           contactUrl=BASE_URL+"contact",
                                           quoteAttrib='''Congratulations;
                                                      you've authorized
                                                      Timing.Is to access your
                                                      Google Calendar data! To
                                                      revoke authorization
                                                      visit your Google account
                                                      @ ''',
                                           link='''
                                   https://myaccount.google.com/permissions''',
                                           linktext='''
                                   https://myaccount.google.com/permissions''',
                                           )

        elif request.method == 'GET':
            return render_template('forms_template.html', form=form,
                                   homeBttnClass="active",
                                   homeUrl=BASE_URL,
                                   aboutUrl=BASE_URL+"about",
                                   contactUrl=BASE_URL+"contact",
                                   quoteAttrib='''Congratulations; you've
                                                      authorized Timing.Is to
                                                      access your Google
                                                      Calendar data! To revoke
                                                      authorization visit your
                                                      Google account @ ''',
                                   link='''
                                   https://myaccount.google.com/permissions''',
                                   linktext='''
                                   https://myaccount.google.com/permissions''',
                                   )


@app.route('/callback')
def callback():
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, SCOPE, REDIRECT_URI)
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        code_uri = str(redirect(auth_uri))
        code = re.search('([^\?code=].+)', code_uri).group(1)
        # http://regexr.com/3ev67

        return redirect(auth_uri)
    else:
        code = request.args.get('code')
        credentials = flow.step2_exchange(code)
        session['credentials'] = credentials.to_json()

        return redirect(url_for('google_oauth2'))


@app.route('/about')
def about_page():
    return render_template('template.html',
                           aboutBttnClass="active",
                           homeUrl=BASE_URL,
                           aboutUrl=BASE_URL+"about",
                           contactUrl=BASE_URL+"contact",
                           quoteText='About',
                           quoteAttrib='',
                           subheading1='''Read-only parsing of your calendar
                                          data''',
                           subtext1='''Timing.is will not store your data. It
                                        will produce summary charts describing
                                        the amount and percent of of total for
                                        all unique events by calendar or time
                                        spent in various categories determined
                                        by a \'tag\'of your choosing, which can
                                        be any word or phrase that you want to
                                        use. Activity domains, such as
                                        physical, social, spiritual or mental;
                                        categorical markers, like professional,
                                        personal or communal.''',
                           subheading2='''Source Code Available on Github''',
                           subtext2='''https://github.com/eayoungs/Timing.is\n
                                        The underlying functionality is
                                        provided by by the GeePal library:\n
                                        https://pypi.python.org/pypi/geepal''',
                           appBttnUrl=BASE_URL+"google_oauth2"
                           )


@app.route('/contact')
def contact_page():
    return render_template('template.html',
                           contactBttnClass="active",
                           homeUrl=BASE_URL,
                           aboutUrl=BASE_URL+"about",
                           contactUrl=BASE_URL+"contact",
                           quoteText='Contact',
                           quoteAttrib='',
                           subheading1='Google Voice',
                           subtext1='503 468 7021',
                           appBttnUrl=BASE_URL+"google_oauth2"
                           )


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')
