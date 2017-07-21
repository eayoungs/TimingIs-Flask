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
from wtforms import (TextField, IntegerField, TextAreaField, SubmitField,
                     SelectField, SelectMultipleField)
from wtforms import validators, ValidationError


class CalendarSelectForm(Form):
    """  """
   
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
    Tag = TextField('Tag', [validators.DataRequired()])
    billing_rate = TextField('Billing Rate')
    provider_email = TextField('Provider Email')
    provider_name = TextField('Provider Name')
    provider_street = TextField('Provider Street')
    provider_city = TextField('Provider City')
    provider_state = TextField('Provier State')
    provider_country = TextField('Provider Country')
    provider_post_code = TextField('Provider Postal Code')
    provider_tax_number = TextField('Provider Tax Number')
    StartDate = TextField("Start Date")
    EndDate = TextField("End Date")
    
    submit = SubmitField("Send")
