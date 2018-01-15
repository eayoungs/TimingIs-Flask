#!/usr/bin/env python

""" This module creates a webisite using the Flask webframework and the Google
    API implementation of the OAuth 2.0 authentication protocol to allow the
    app to parse your Google Calendars. It also uses a library, written by the
    same author, to provide summary statistics about your events. """

__author__ = "Eric Allen Youngson"
__email__ = "eayoungs@gmail.com"
__copyright__ = "Copyright 2017 Eric Youngson"
__license__ = "Apache 2.0"

from flask_wtf import Form
from wtforms import (TextField, IntegerField, TextAreaField, SubmitField,
                     SelectField, SelectMultipleField, validators,
                     ValidationError)


class CalendarSelectForm(Form):
    """ """

    Calendars = SelectMultipleField('Calendar')

    DateRange = SelectField('Date Range',
                            choices=[('day', 'Today'), ('week', 'This Week'),
                                     ('month', 'This Month'),
                                     ('year', 'Year')
                                     ]
                            )
    """
    , ('yesterday', 'Yesterday'),
    ('lastWeek', 'Last Week'),
    ('lastMonth', 'Last Month')"""

    StartDate = TextField("Start Date")  # TODO: (eayoungs@gmail)
    """
    ,[validators.Required("Please enter a valid date
    range in iso8601 format")])
    """

    EndDate = TextField("End Date")
    """
    ,[validators.Required("Please enter a valid date
    range in iso8601 format")])
    """

    Tag = TextField("Tag")  # ,
    # [validators.Required("Enter a tag to filter events by")])

    billing_rate = TextField('Billing Rate')
    provider_email = TextField('Provider Email')
    provider_name = TextField('Provider Name')
    provider_street = TextField('Provider Street')
    provider_city = TextField('Provider City')
    provider_state = TextField('Provider State')
    provider_country = TextField('Provider Country')
    provider_post_code = TextField('Provider Postal Code')
    provider_tax_rate = TextField('Provider Tax Rate')
    invoice_id = TextField('Invoice Number')
    invoice_due_date = TextField('Days Until Invoice Due')
    client_email = TextField('Client Email')

    submit = SubmitField("Send")
