from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from flask import Flask, render_template, session, url_for, request, redirect
import re
import uuid
import json
import os
from bootstrap_flask import create_app
import httplib2
from googleapiclient import discovery


app = create_app()
app.secret_key = str(uuid.uuid4())


@app.route('/')
def main():
  return render_template('index.html')

@app.route('/google_oauth2')
def google_oauth2():
    if 'credentials' not in session:
        return redirect(url_for('callback'))
    credentials = OAuth2Credentials.from_json(session['credentials'])

    if credentials.access_token_expired:
        return redirect(url_for('callback'))

    else: # https://developers.google.com/api-client-library/python/auth/web-app
      http_auth = credentials.authorize(httplib2.Http())
      service = discovery.build('calendar', 'v3', http=http)
      return render_template('g-oath2-landing.html')
    

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


if __name__ == '__main__':
  app.debug = False
  app.run()
