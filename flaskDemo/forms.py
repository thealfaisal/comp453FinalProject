from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField,validators,DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp,Required
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import Customer, Location, Reservation, Vehicle, Style, Trim, Brand, Model
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField

locs = Location.query.with_entities(Location.locationID,Location.locationName).distinct()
styles = Style.query.with_entities(Style.stylename).distinct()
trims = Trim.query.with_entities(Trim.trimlevel).distinct()
brands = Brand.query.with_entities(Brand.brandname).distinct()
models = Model.query.with_entities(Model.ModelName).distinct()
# ssns = Department.query.with_entities(Department.mgr_ssn).distinct()
#  or could have used ssns = db.session.query(Department.mgr_ssn).distinct()
# for that way, we would have imported db from flaskDemo, see above
transm = [(0,"Manual"),(1,"Automatic")]

myChoices2 = [(row[1],row[1]) for row in locs]  # change
#myChoices3 = [(row[0],row[0]) for row in locs]
# """
# results=list()
# for row in ssns:
#     rowDict=row._asdict()
#     results.append(rowDict)
# myChoices = [(row['mgr_ssn'],row['mgr_ssn']) for row in results]
# """


styleChoices = [(row[0],row[0]) for row in styles]  # change
trimChoices = [(row[0],row[0]) for row in trims]  # change
brandChoices = [(row[0],row[0]) for row in brands]  # change
modelChoices = [(row[0],row[0]) for row in models]  # change
tranChoices = [(row[1],row[1]) for row in transm]  # change
"""
results=list()
for row in ssns:
    rowDict=row._asdict()
    results.append(rowDict)
myChoices = [(row['mgr_ssn'],row['mgr_ssn']) for row in results]
"""

regex1='^((((19|20)(([02468][048])|([13579][26]))-02-29))|((20[0-9][0-9])|(19[0-9][0-9]))-((((0[1-9])'
regex2='|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))$'
regex=regex1 + regex2




class RegistrationForm(FlaskForm):
    fullname = StringField('Name*',
                           validators=[DataRequired(), Length(min=2, max=30)])
    phonenumber = StringField('Phone Number*', validators=[DataRequired()])
    username = StringField('Username*',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email address*',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password*',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reserve Now >')

    def validate_username(self, username):
        user = Customer.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Customer.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
# """
#     def validate_phonenumber(form, phonenumber):
#         if len(phonenumber.data) > 16:
#             raise ValidationError('Invalid phone number.')
#         try:
#             input_number = phonenumber.parse(phonenumber.data)
#             if not (phonenumber.is_valid_number(input_number)):
#                 raise ValidationError('Invalid phone number.')
#         except:
#             input_number = phonenumber.parse("+1"+phonenumber.data)
#             if not (phonenumber.is_valid_number(input_number)):
#                 raise ValidationError('Invalid phone number.')
#
# """
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    Pickingup = SelectField("Picking up", choices=myChoices2)
    Dropoff = SelectField("Dropping off", choices=myChoices2)
    Pickupdate = DateField("Pickup Date", validators=[Required()])
    Pickuptime = TimeField("Pickup Time",validators=[Required()])
    Dropoffdate = DateField("Dropoff Date", validators=[Required()])
    Dropofftime = TimeField("Dropoff Time",validators=[Required()])
    submit = SubmitField('Search')

class VehicleForm(FlaskForm):
    BrandName = SelectField("Brand", choices=brandChoices)
    PlateNumber = StringField('PlateNumber',validators=[DataRequired()])
    Model = SelectField("Model", choices=modelChoices)
    Year = IntegerField("Year",validators=[DataRequired()])
    Style = SelectField("Style", choices=styleChoices)
    Transmission = SelectField("Transmission", choices=tranChoices)
    TrimLevel = SelectField("Trim", choices=trimChoices)
    Rate = DecimalField(places=2, validators=[DataRequired()])
    locationName = SelectField("Location", choices=myChoices2)
    submit = SubmitField('Add')
#coerce=int
class LocationForm(FlaskForm):
    LocationName = StringField('Location Name',validators=[DataRequired()])
    City = StringField('City',validators=[DataRequired()])
    State = StringField('State',validators=[DataRequired()])
    Zipcode = StringField('Zipcode',validators=[DataRequired()])
    submit = SubmitField('Add')


"""
def __init__(self, *args, **kwargs):
    kwargs['csrf_enabled'] = False
    super(SearchForm, self).__init__(*args, **kwargs)
"""

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    address = StringField('Address')
    city = StringField('City')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Customer.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Customer.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')





#
# """
# class PostForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired()])
#     content = TextAreaField('Content', validators=[DataRequired()])
#     submit = SubmitField('Post')
#
#
# class DeptUpdateForm(FlaskForm):
#
# #    dnumber=IntegerField('Department Number', validators=[DataRequired()])
#     dnumber = HiddenField("")
#
#     dname=StringField('Department Name:', validators=[DataRequired(),Length(max=15)])
# #  Commented out using a text field, validated with a Regexp.  That also works, but a hassle to enter ssn.
# #    mgr_ssn = StringField("Manager's SSN", validators=[DataRequired(),Regexp('^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$', message="Please enter 9 digits for a social security.")])
#
# #  One of many ways to use SelectField or QuerySelectField.  Lots of issues using those fields!!
#     mgr_ssn = SelectField("Manager's SSN", choices=myChoices)  # myChoices defined at top
#
# # the regexp works, and even gives an error message
# #    mgr_start=DateField("Manager's Start Date:  yyyy-mm-dd",validators=[Regexp(regex)])
# #    mgr_start = DateField("Manager's Start Date")
#
# #    mgr_start=DateField("Manager's Start Date", format='%Y-%m-%d')
#     mgr_start = DateField("Manager's start date:", format='%Y-%m-%d')  # This is using the html5 date picker (imported)
#     submit = SubmitField('Update this department')
#
#
# # got rid of def validate_dnumber
#
#     def validate_dname(self, dname):    # apparently in the company DB, dname is specified as unique
#          dept = Department.query.filter_by(dname=dname.data).first()
#          if dept and (str(dept.dnumber) != str(self.dnumber.data)):
#              raise ValidationError('That department name is already being used. Please choose a different name.')
#
#
# class DeptForm(DeptUpdateForm):
#
#     dnumber=IntegerField('Department Number', validators=[DataRequired()])
#     submit = SubmitField('Add this department')
#
#     def validate_dnumber(self, dnumber):    #because dnumber is primary key and should be unique
#         dept = Department.query.filter_by(dnumber=dnumber.data).first()
#         if dept:
#             raise ValidationError('That department number is taken. Please choose a different one.')
# """
