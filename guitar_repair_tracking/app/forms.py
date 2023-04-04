from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, TelField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from wtforms.widgets import TextArea
from app.models import Customer
# create form classes

class CustomerForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(max=20)])
    phone = TelField('Phone', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Add')

class GuitarForm(FlaskForm):
    customer_id = SelectField('Customer', coerce=int)
    brand = StringField('Guitar Brand', validators=[DataRequired(), Length(max=120)])
    model = StringField('Guitar Model', validators=[DataRequired(), Length(max=120)])
    serial_number = StringField('Serial Number', validators=[Length(max=120)])
    description = StringField('Repair Description', widget=TextArea(), validators=[DataRequired(), Length(max=250)])
    repair_status = StringField('Repair Status', validators=[DataRequired(), Length(max=120)])
    
    submit = SubmitField('Create')

    def __init__(self, *args, **kwargs):
        super(GuitarForm, self).__init__(*args, **kwargs)
        self.customer_id.choices = [(customer.id, customer.firstname + ' ' + customer.lastname) for customer in Customer.query.order_by('firstname').all()]
