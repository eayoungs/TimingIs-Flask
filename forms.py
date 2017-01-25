from flask_wtf import Form
from wtforms import TextField
from wtforms import validators, ValidationError


class ContactForm(Form):
   name = TextField("Name Of Student", [validators.Required(
                                                   "Please enter your name.")])
