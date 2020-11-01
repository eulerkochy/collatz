from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, DecimalField, BooleanField 
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

    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    type = SelectField('Type', choices = ['Fabric Manufacturer', 'Garment Assembler', 'Retailer', 'User'], validators = [InputRequired()])
    submit = SubmitField('Login')

class InputFibreForm(FlaskForm):
    source_location = StringField('Location of origin of Fibre', validators = [InputRequired()])
    manufacturer = StringField('Manufacturer name', validators = [InputRequired()])
    contact_of_manufacturer = IntegerField('Contact number of manufacturer', validators = [InputRequired()])
    fibre = SelectField('Fibre', choices = ['Cotton', 'Silk', 'Polyester'], validators = [InputRequired()])
    weight = DecimalField('Weight in kgs', validators = [InputRequired()])
    cost_per_unit = DecimalField('Cost per unit (INR)', validators = [InputRequired()])
    rebate = DecimalField('Rebate', validators = [InputRequired()])
    type_of_fibre = SelectField('Type of fibre', choices = ['Organic', 'Inorganic'], validators = [InputRequired()])
    submit = SubmitField('Add Fibre to inventory')

class FabricProducedForm(FlaskForm):
    fabric_name = StringField("Fabric Name", validators = [InputRequired()])
    number_fibres_used = IntegerField('Number of fibres used', validators = [InputRequired()])
    fibre1_id = IntegerField('Fibre 1 ID', validators = [InputRequired()])
    fibre1_weight_used = DecimalField('Weight of Fibre 1 used', validators = [InputRequired()])
    fibre1_weight_wasted = DecimalField('Weight of Fibre 1 wasted', validators = [InputRequired()])
    area = DecimalField('Area of fabric produced', validators = [InputRequired()])
    weight = DecimalField('Weight of fabric produced', validators = [InputRequired()])
    production_cost_per_unit = DecimalField('Production cost per unit area', validators = [InputRequired()])
    submit = SubmitField('Add Fabric Produced')

class TransactionWithGarmentAssemblerForm(FlaskForm):
    fabric_id = IntegerField('Fabric Id', validators = [InputRequired()])
    area = DecimalField('Area sold in sqaure meters', validators = [InputRequired()])
    weight = DecimalField('Weight sold in kgs', validators = [InputRequired()])
    sold_to = IntegerField('Buyer', validators = [InputRequired()])
    selling_price_per_unit = DecimalField('Selling price per unit (INR)', validators = [InputRequired()])
    rebate = DecimalField('Rebate', validators = [InputRequired()])
    submit = SubmitField('Add transaction')

class InputForm(FlaskForm):
    transaction_id = IntegerField('Transaction ID', validators = [InputRequired()])
    submit = SubmitField('Submit')

class ConfirmInputForm(FlaskForm):
    confirm = SubmitField('Confirm')
    cancel = SubmitField('Cancel')

class GarmentProducedForm(FlaskForm):
    garment_name = StringField('Name of garment', validators = [InputRequired()])
    number_fabrics_used = IntegerField('Number of fabrics used', validators = [InputRequired()])
    fabric1_id = IntegerField('Fabric 1 ID', validators = [InputRequired()])
    fabric1_weight_used = DecimalField('Weight of Fabric 1 used', validators = [InputRequired()])
    fabric1_weight_wasted = DecimalField('Weight of Fabric 1 wasted', validators = [InputRequired()])
    fabric2_id = IntegerField('Fabric 2 ID', validators = [InputRequired()])
    fabric2_weight_used = DecimalField('Weight of Fabric 2 used', validators = [InputRequired()])
    fabric2_weight_wasted = DecimalField('Weight of Fabric 2 wasted', validators = [InputRequired()])
    trimming_technique = StringField('Trimming technique', validators = [InputRequired()])
    sewing_technique = StringField('Sewing Technique', validators = [InputRequired()])
    printing_technique = StringField('Printing Technique', validators = [InputRequired()])
    chemical_finish = StringField('Chemical Finish', validators = [InputRequired()])
    screen_printing_or_heat_transfer = BooleanField('Screen printing or heat transfer label')
    quantity_produced = IntegerField('Quantity produced', validators = [InputRequired()])
    production_cost_per_unit = DecimalField('Production cost per piece', validators = [InputRequired()])
    submit = SubmitField('Add garment produced')

class TransactionWithRetailerForm(FlaskForm):
    garment_id = IntegerField('Garment ID', validators = [InputRequired()])
    quantity_sold = IntegerField('Quantity sold', validators = [InputRequired()])
    sold_to = IntegerField('Buyer', validators = [InputRequired()])
    selling_price_per_unit = DecimalField('Selling price per piece', validators = [InputRequired()])
    rebate = DecimalField('Rebate', validators = [InputRequired()])
    submit = SubmitField('Add transaction')

class TransactionWithUserForm(FlaskForm):
    garment_id = IntegerField('Garment ID', validators = [InputRequired()])
    quantity_sold = IntegerField('Quantity sold', validators = [InputRequired()])
    sold_to = IntegerField('Buyer', validators = [InputRequired()])
    selling_price_per_unit = DecimalField('Selling price per piece', validators = [InputRequired()])
    send_back = BooleanField('Will buyer return garment after use?', validators = [InputRequired()])
    send_back_after_months = IntegerField('No. of months after which product will be returned')
    packaging_info = StringField('Packaging information', validators = [InputRequired()])
    submit = SubmitField('Submit')