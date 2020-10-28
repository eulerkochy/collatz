from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, DecimalField, SelectMultipleField, FieldList, FormField 
from wtforms.validators import InputRequired, Email, EqualTo
from fabric_manufacturer import RawFibre

states = ["State1","State2"]


class SignUpUserForm(FlaskForm):
    name = StringField('Full Name', validators = [InputRequired()])
    email = StringField('Email', validators = [InputRequired(), Email()])
    contact_number = IntegerField('Contact Number', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class SignUpForm(FlaskForm):
    name_of_company = StringField('Name of the Company', validators = [InputRequired()])
    state = SelectField('State', choices = states, validators = [InputRequired()])
    city = StringField('City', validators = [InputRequired()])
    stakeholder_type = SelectField('Organization Type', choices = ['Fabric Manufacturer', 'Garment Assembler', 'Retailer'], validators = [InputRequired()])
    contact_number = IntegerField('Contact Number', validators = [InputRequired()])
    address = TextAreaField('Address', validators = [InputRequired()])
    email = StringField('Email', validators = [InputRequired(), Email()])
    year_of_estab = IntegerField('Year of Estabslishment', validators = [InputRequired()])
    annual_turnover = IntegerField('Annual Turnover', validators = [InputRequired()])
    employee_strength = IntegerField('Employee Strength', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [InputRequired(), EqualTo('password')]) 

    poc1_name = StringField('Name of POC1', validators = [InputRequired()])
    poc1_contact_number = IntegerField('Contact Number of POC1', validators = [InputRequired()])
    poc1_email = StringField('Email of POC1', validators = [InputRequired(), Email()])
    poc1_designation = StringField('Designation of POC1', validators = [InputRequired()])

    poc2_name = StringField('Name of POC2', validators = [InputRequired()])
    poc2_contact_number = IntegerField('Contact Number of POC2', validators = [InputRequired()])
    poc2_email = StringField('Email of POC2', validators = [InputRequired(), Email()])
    poc2_designation = StringField('Designation of POC2', validators = [InputRequired()])

    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    type = SelectField('Type', choices = ['Fabric Manufacturer', 'Garment Assembler', 'Retailer', 'User'], validators = [InputRequired()])
    submit = SubmitField('Login')

class FibreForm(FlaskForm):
    source_location = StringField('Location of origin of Fibre', validators = [InputRequired()])
    manufacturer = StringField('Manufacturer name', validators = [InputRequired()])
    contact_of_manufacturer = IntegerField('Contact number of manufacturer', validators = [InputRequired()])
    fibre = SelectField('Fibre', choices = ['Cotton', 'Silk', 'Polyester'], validators = [InputRequired()])
    weight = DecimalField('Weight in kgs', validators = [InputRequired()])
    cost_per_unit = DecimalField('Cost per unit (INR)', validators = [InputRequired()])
    rebate = DecimalField('Rebate', validators = [InputRequired()])
    type_of_fibre = SelectField('Type of fibre', choices = ['Organic', 'Inorganic'], validators = [InputRequired()])
    submit = SubmitField('Add Fibre')

def selections(limit):
    message = "Select "+limit+" fields"
    def _selections(form, field):
        l = field.data and len(field.data) or 0
        if l!=limit:
            raise ValidationError(message)
    return _selections

global count

class Quantities(Form):
    quantity = IntegerField('Quantity of fibre', validators = [InputRequired()])


# class FabricProducedForm(FlaskForm):
#     number_fibres_used = IntegerField('Number of fibres used')
#     # fibres_used = SelectMultipleField(
#     #     'Fibre',
#     #     choices = [
#     #         (f.fibre, f.manufacturer, f.rowid) for f in user_in_session.fibres_owned
#     #     ],
#     #     validators = [InputRequired(), selections(number_fibres_used.data)]
#     # )
#     quantities_in_order = FieldList(
#         FormField(Quantities),
#         min_entries = number_fibres_used.data,
#         max_entries = number_fibres_used.data
#     )
#     length_of_fabric = DecimalField('Length of fabric (meters)', validators = [InputRequired()])