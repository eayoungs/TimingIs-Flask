
# # http://flask.pocoo.org/docs/0.12/patterns/wtforms/
# from wtforms import Form, BooleanField, StringField, PasswordField, validators
# 
# 
# class RegistrationForm(Form):
#     username = StringField('Username', [validators.Length(min=4, max=25)])
#     email = StringField('Email Address', [validators.Length(min=6, max=35)])
#     password = PasswordField('New Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords must match')
#     ])
#     confirm = PasswordField('Repeat Password')
#     accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

from wtforms import Form, SelectMultipleField


class LanguageForm(Form):
    dateRange = SelectMultipleField(u'Time Period', choices=[('day', 'day'),
                                                             ('week', 'week')])
