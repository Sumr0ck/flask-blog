from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import InputRequired, ValidationError, DataRequired, EqualTo, Email
from models import User


class PostForm(Form):
    title = StringField('Title', validators=[InputRequired('Empty field title')])
    body = TextAreaField('Body', validators=[InputRequired('Empty field body')])


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')