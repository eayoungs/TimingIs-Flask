from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
import flask
import re
import uuid
import json
import os
# import httplib2
# from googleapiclient import discovery


app = flask.Flask(__name__)

app.secret_key = str(uuid.uuid4())


@app.route('/')
def main():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('callback'))
    credentials = OAuth2Credentials.from_json(flask.session['credentials'])

    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))

    else:
      return flask.render_template('g-oath2-landing.html')
    

@app.route('/callback')
def callback():
    flow = OAuth2WebServerFlow(client_id=os.environ.get('CLIENT_ID'),
                           client_secret=os.environ.get('CLIENT_SECRET'),
                           scope=os.environ.get('SCOPE'),
                           redirect_uri=os.environ.get('REDIRECT_URI')
                           )
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        code_uri = str(flask.redirect(auth_uri))
        code = re.search('([^\?code=].+)', code_uri).group(1)
        # http://regexr.com/3ev67

        return flask.redirect(auth_uri)
    else:
        code = flask.request.args.get('code')
        credentials = flow.step2_exchange(code)
        flask.session['credentials'] = credentials.to_json()

        return flask.redirect(flask.url_for('main'))


if __name__ == '__main__':
  app.debug = True
  app.run()
