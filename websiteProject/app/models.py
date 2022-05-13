from unicodedata import name
from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password1 = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    def __repr__(self):
        return f'<Email: {self.email}, Name: {self.name}>'



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(64))
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<{self.user_id}, {self.timestamp}: {self.body}>'

class LoginForm(FlaskForm):
   #user = StringField('Name', validators=[DataRequired()])
   name = StringField('Email', validators=[DataRequired()])
   password = PasswordField('Password', validators=[DataRequired()])
   remember_me = BooleanField('Remember Me')
   submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    user = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])