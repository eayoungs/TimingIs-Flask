#!/usr/bin/env python

__author__ = "Eric Allen Youngson"
__email__ = "eayoungs@gmail.com"
__copyright__ = "Copyright 2017"
__license__ = "Apache 2.0"

""" This module creates a webisite using the Flask webframework and the Google
    API implementation of the OAuth 2.0 authentication protocol to allow the
    app to parse your Google Calendars. It also uses a library, written by the
    same author, to provide summary statistics about your events. """


from flask import Flask
from flask_bootstrap import Bootstrap


def create_app():
  app = Flask(__name__)
  Bootstrap(app)

  return app
