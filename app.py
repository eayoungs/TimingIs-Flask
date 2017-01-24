from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from flask import Flask, render_template, session, url_for, request, redirect
import re
import uuid
import json
import os
from bootstrap_flask import create_app
import httplib2
from googleapiclient import discovery
# import forms

import get_events as ge


app = create_app()
app.secret_key = str(uuid.uuid4())

baseUrl = "http://timing.is/"

@app.route('/')
def main():
  return render_template('template.html',
                         homeBttnClass="active",
                         homeUrl=baseUrl,
                         aboutUrl=baseUrl+"about",
                         contactUrl=baseUrl+"contact",
                         quoteText='"This Moment is All There Is"',
                         quoteAttrib='--Rumi',
                         subheading1='Build your routine, your way',
                         subtext1='Find out where your spend your time, setgoals and check in on your progress with minimal effort--all in from withing the calendar you already know & love: Google Calendar',
                         subheading2="Show the muse you're serious",
                         subtext2='You have to show up for your dreams; no one can do it for you but we can give you the tools to stay present',
                         appBttnUrl=baseUrl+"google_oauth2")


@app.route('/google_oauth2')
def google_oauth2():
    if 'credentials' not in session:
        return redirect(url_for('callback'))
    credentials = OAuth2Credentials.from_json(session['credentials'])

    if credentials.access_token_expired:
        return redirect(url_for('callback'))

    else:# https://developers.google.com/api-client-library/python/auth/web-app
        http_auth = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http_auth)

        page_token = None# https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list#try-it
        while True:
            calendar_list = service.calendarList().list(
                                                pageToken=page_token).execute()
            calendarsDct = {}
            for calendar_list_entry in calendar_list['items']:
                calendarsDct[calendar_list_entry['summary']] = calendar_list_entry['id']
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

        evStart_evEnd = ge.event_range(relRange='day')
        gtEvents = ge.get_events(service, evStart_evEnd, calendarsDct)

        return render_template('forms_template.html',
                               homeBttnClass="active",
                               homeUrl=baseUrl,
                               aboutUrl=baseUrl+"about",
                               contactUrl=baseUrl+"contact",
                               quoteAttrib="Congratulations; you've authorized Timing.Is to access your Google Calendar data! To revoke authorization visit your Google account @ ",
                               subheading1=calendarsDct.keys(),
                               subtext1=gtEvents,
                               link="https://myaccount.google.com/permissions",
                               linktext="https://myaccount.google.com/permissions")
    

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
                         subtext1="Timing.Is will not store your data. It will produce summary charts describing the amount and percent of of total for all unique events, by calendar or time spent in various categories determined by a 'tag'of your choosing, which can be any word or phrase that you want to use. Activity domains, such as physical, social, spiritual or mental; categorical markers, like professional, personal or communal. If you want tomodify the code and create your own custom algorithms, you can. Right there in the same page where theresults appear.",
                         appBttnUrl=baseUrl+"google_oauth2")


@app.route('/contact')
def contact_page():
  return render_template('template.html',
                         contactBttnClass="active",
                         homeUrl=baseUrl,
                         aboutUrl=baseUrl+"about",
                         contactUrl=baseUrl+"contact",
                         quoteText='Contact',
                         quoteAttrib='',
                         subheading1='',
                         subtext1="",
                         appBttnUrl=baseUrl+"google_oauth2")



if __name__ == '__main__':
  app.debug = False
  app.run()
