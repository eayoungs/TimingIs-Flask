from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, SelectField, SelectMultipleField


from wtforms import validators, ValidationError

class CalendarSelectForm(Form):
   """ """
   
   Calendars = SelectMultipleField('Calendar')

   DateRange = SelectField('Date Range',
                          choices = [('day', 'Today'), ('week', 'This Week')])
   
   StartDate = TextField("Start Date")#,[validators.Required("Please enter a valid date range in iso8601 format")])

   EndDate = TextField("End Date")#,[validators.Required("Please enter a valid date range in iso8601 format")])
   
   Tag = TextField("Tag")#,
                   #[validators.Required("Enter a tag to filter events by")])

   submit = SubmitField("Send")
