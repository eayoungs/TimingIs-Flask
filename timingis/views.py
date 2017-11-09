from timingis import app
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials

import re
import uuid
import json
import os

import httplib2
from googleapiclient import discovery

from geepal import get_events as ge
from geepal import dfsort as dfs
import invoice


#app = Flask(__name__)#app = create_app()
app.secret_key = str(uuid.uuid4())
app.config.from_pyfile('settings.cfg')
BASE_URL = app.config['BASE_URL']
CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']
SCOPE = app.config['SCOPE']
REDIRECT_URI = app.config['REDIRECT_URI']


@app.route('/')
def index():
    return 'Hello World!'