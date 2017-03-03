#!/usr/bin/env python

__author__ = "Eric Allen Youngson"
__email__ = "eayoungs@gmail.com"
__copyright__ = "Copyright 2017"
__license__ = "Apache 2.0"

""" This module creates a webisite using the Flask webframework and the Google
    API implementation of the OAuth 2.0 authentication protocol to allow the
    app to parse your Google Calendars. It also uses a library, written by the
    same author, to provide summary statistics about your events. """


from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from flask import Flask, render_template, session, url_for, request, redirect
import re
import uuid
import json
import os
from bootstrap_flask import create_app
import httplib2
from googleapiclient import discovery

from forms import CalendarSelectForm
import get_events as ge
import dfsort as dfs


app = create_app()
app.secret_key = str(uuid.uuid4())

baseUrl = "https://timingis.herokuapp.com/"

@app.route('/')
def main():
  return render_template('template.html',
                         homeBttnClass="active",
                         homeUrl=baseUrl,
                         aboutUrl=baseUrl+"about",
                         contactUrl=baseUrl+"contact",
                         quoteText='Everything',
                         quoteAttrib='"This Moment is All there Is" --Rumi',
                         subheading1='Build your routine, your way',
                         subtext1='Find out where your spend your time, setgoals and check in on your progress with minimal effort--all in from withing the calendar you already know & love: Google Calendar',
                         subheading2="Show the muse you're serious",
                         subtext2='You have to show up for your dreams; no one can do it for you but we can give you the tools to stay present',
                         appBttnUrl=baseUrl+"google_oauth2")


@app.route('/google_oauth2', methods = ['GET', 'POST'])
def google_oauth2():
    if 'credentials' not in session:
        return redirect(url_for('callback'))
    credentials = OAuth2Credentials.from_json(session['credentials'])

    if credentials.access_token_expired:
        return redirect(url_for('callback'))

    else:
        form = CalendarSelectForm()
        # https://developers.google.com/api-client-library/python/auth/web-app

        http_auth = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http_auth)
        
        page_token = None# https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list#try-it
        while True:
            calendar_list = service.calendarList().list(
                                                pageToken=page_token).execute()
            calendarsDct = {}
            for calendar_list_entry in calendar_list['items']:
                calendarsDct[ # Object creation order seems to be reversed:
                              # just going with it here...¯\_(ツ)_/¯ (see ln80)
                calendar_list_entry['id']] = calendar_list_entry['summary']
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        form.Calendars.choices = calendarsDct.items()

        if request.method ==  'POST':
            if form.validate() == False:
                return render_template('forms_template.html', form=form,
                                       homeBttnClass="active",
                                       homeUrl=baseUrl,
                                       aboutUrl=baseUrl+"about",
                                       contactUrl=baseUrl+"contact",
                                       quoteAttrib="Congratulations; you've authorized Timing.Is to access your Google Calendar data! To revoke #authorization visit your Google account @ ",
                                       link="https://myaccount.google.com/permissions",
                                       linktext="https://myaccount.google.com/permissions"
                                       )
            else: # Reverse logical order of dicitonary (see ln63)
                calendarsSelectedDct = {value:key for key,value in
                          form.Calendars.choices if key in form.Calendars.data}
                evStart_evEnd = ge.event_range(relRange=form.DateRange.data)
                evStartEvEnd_eventsDct = ge.get_events(service, evStart_evEnd,
                                                       calendarsSelectedDct)
                (evStart_evEnd, eventsDct) = evStartEvEnd_eventsDct
                evStartEvEnd_calEvDfsDct = dfs.add_durations(
                                                        evStartEvEnd_eventsDct)
                calWorkTypesDct={}
                titles=[]
                tables=[]
                for key,value in calendarsSelectedDct.items():
                    workTypesDct = dfs.get_work_types(evStartEvEnd_calEvDfsDct,
                                                      key)
                    calDursSmry = dfs.get_cals_durs(workTypesDct)
                    calDursDF_fmatSumCumCalTotHrs = dfs.summarize_cals_durs(
                                                                   calDursSmry)
                    (calDursDF,
                     fmatSumCumCalTotHrs) =calDursDF_fmatSumCumCalTotHrs

                    titles.append(key)
                    tables.append(calDursDF.to_html())

                    #calWorkTypesDct[key] = (calDursDF.to_html(),
                    #                        fmatSumCumCalTotHrs)

                return render_template('forms_filled_template.html', form=form,
                                       titles=titles,
                                       tables=tables,
                                       homeBttnClass="active",
                                       homeUrl=baseUrl,
                                       aboutUrl=baseUrl+"about",
                                       contactUrl=baseUrl+"contact",
                                       quoteAttrib="Congratulations; you've authorized Timing.Is to access your Google Calendar data! To revoke #authorization visit your Google account @ ",
                                       subheading1=evStart_evEnd,
                                       link="https://myaccount.google.com/permissions",
                                       linktext="https://myaccount.google.com/permissions"
                                       )

        elif request.method == 'GET':
            return render_template('forms_template.html', form=form,
                                   homeBttnClass="active",
                                   homeUrl=baseUrl,
                                   aboutUrl=baseUrl+"about",
                                   contactUrl=baseUrl+"contact",
                                   quoteAttrib="Congratulations; you've authorized Timing.Is to access your Google Calendar data! To revoke #authorization visit your Google account @ ",
                                   link="https://myaccount.google.com/permissions",
                                   linktext="https://myaccount.google.com/permissions"
                                   )

        """
        if request.method == 'GET':
            if form.validate() == False:
               flash('All fields are required.')
               return render_template('contact.html', form = form) 
            elif request.method == 'GET':
               return render_template('contact.html', form = form)
            else:
               return render_template('success.html')
        """


@app.route('/callback')
def callback():
    flow = OAuth2WebServerFlow(client_id=os.environ.get('CLIENT_ID'),
                           client_secret=os.environ.get('CLIENT_SECRET'),
                           scope=os.environ.get('SCOPE'),
                           redirect_uri=os.environ.get('REDIRECT_URI')
                           )
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


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = forms.RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         user = User(form.username.data, form.email.data,
#                     form.password.data)
#         db_session.add(user)
#         flash('Thanks for registering')
#         return redirect(url_for('login'))
#     return render_template('forms_template.html', form=form,
#                            homeBttnClass="active",
#                            homeUrl=baseUrl,
#                            aboutUrl=baseUrl+"about",
#                            contactUrl=baseUrl+"contact",)


@app.route('/about')
def about_page():
  return render_template('template.html',
                         aboutBttnClass="active",
                         homeUrl=baseUrl,
                         aboutUrl=baseUrl+"about",
                         contactUrl=baseUrl+"contact",
                         quoteText='About',
                         quoteAttrib='',
                         subheading1='Read-only parsing of your calendar data',
                         subtext1="Timing.Is will not store your data. It will produce summary charts describing the amount and percent of of total for all unique events, by calendar or time spent in various categories determined by a 'tag'of your choosing, which can be any word or phrase that you want to use. Activity domains, such as physical, social, spiritual or mental; categorical markers, like professional, personal or communal.",
                         appBttnUrl=baseUrl+"google_oauth2"
                         )

@app.route('/contact')
def contact_page():
  return render_template('template.html',
                         contactBttnClass="active",
                         homeUrl=baseUrl,
                         aboutUrl=baseUrl+"about",
                         contactUrl=baseUrl+"contact",
                         quoteText='Contact',
                         quoteAttrib='',
                         subheading1='Google Voice',
                         subtext1='503 468 7021',
                         appBttnUrl=baseUrl+"google_oauth2"
                         )



if __name__ == '__main__':
  app.debug = False
  app.run()
