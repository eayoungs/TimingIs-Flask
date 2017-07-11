#!/usr/bin/env python

__author__ = "Eric Allen Youngson"
__email__ = "eayoungs@gmail.com"
__copyright__ = "Copyright 2017 Eric Youngson"
__license__ = "Apache 2.0"

""" This module creates a webisite using the Flask webframework and the Google
    API implementation of the OAuth 2.0 authentication protocol to allow the
    app to parse your Google Calendars. It also uses a library, written by the
    same author, to provide summary statistics about your events. """


from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, SelectField, SelectMultipleField
from wtforms import validators, ValidationError


class CalendarSelectForm(Form):
   """ """
   
   Calendars = SelectMultipleField('Calendar')
   DateRange = SelectField('Date Range',
                           choices = [('day', 'Today'), ('week', 'This Week'),
                                      ('month', 'This Month'),
                                      ('year', 'Year')#,
                                      #('yesterday', 'Yesterday'),
                                      #('lastWeek', 'Last Week'),
                                      #('lastMonth', 'Last Month')
                                     ]
                          )
   StartDate = TextField("Start Date", [validators.Length(min=10, max=10)])
   EndDate = TextField("End Date", [validators.Length(min=10, max=10)])
   Tag = TextField("Tag", [validators.Length(min=1, max=30)])    
   submit = SubmitField("Send")
