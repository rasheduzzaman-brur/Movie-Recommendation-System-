from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, email_validator
from model import movieDict
from databaseTable import User



class LoginFrom(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4,max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(),Length(min=4,max=20)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")


class RegisterFrom(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4,max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(),Length(min=4,max=20)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Register")

class UdateProfileFrom(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4,max=20)], render_kw={"placeholder":"Update Username"})
    update = SubmitField("Update")

class DashbordForm(FlaskForm):
    moviename = SelectField('Select movie',validators=[InputRequired()],choices=[(val,val) for val in movieDict.keys()])
    submit = SubmitField("Search")


class UserratingForm(FlaskForm):
    rating = SelectField('Add Review',validators=[InputRequired()],choices=[(1,'OneStar'),(2,'TwoStar'),(3,'ThreeStar'),(4,'FourStar'),(5,'FiveStar')])
    comment = TextAreaField('Comments', validators=[Length(max=200)])
    submit = SubmitField("Submit")