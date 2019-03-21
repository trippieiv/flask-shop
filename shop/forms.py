from flask_wtf import FlaskForm
from wtforms import Form,StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from shop.models import User
from wtforms.fields.html5 import DateField
from datetime import date

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Regexp('^.{6,8}$', message='Your password should be between 6 and 8 characters long.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exist. Please choose a different one.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')




class CheckoutForm(FlaskForm):
    name = StringField('Name on Card', validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    address = StringField('Address',validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postcode = StringField('Postcode',validators=[DataRequired()])
    state = StringField('State',validators=[DataRequired()])
    
    cardNum = StringField('Card Number', validators=[DataRequired(),Regexp('^\d{4}-?\d{4}-?\d{4}-?\d{4}$', message = 'Please use the correct format shown')])
    expmonth = StringField("Expiry Month", validators=[DataRequired(message="Please Enter")])
    expyear = StringField('Expiry year' , validators=[DataRequired(message='Please enter the year')])
    cvv = StringField('CVV',validators=[DataRequired(message='Please enter the year'), Regexp('^[0-9]{3}$', message='Error')])
    submit = SubmitField('Pay')


    
