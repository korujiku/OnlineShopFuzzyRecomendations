from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    age = IntegerField('Age', validators=[DataRequired()])
    interests = SelectMultipleField('Interests',
                                    choices=[('Tech', 'Tech'), ('Fashion', 'Fashion'), ('Sports', 'Sports'),
                                             ('Music', 'Music')])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
