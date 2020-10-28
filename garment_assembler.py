from stakeholder import db

class GarmentAssembler(db.Model):
    name_of_company = db.Column(db.String, unique=True, nullable=False)
    state = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    #TODO verify valid phone number
    contact_number = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, primary_key = True)
    password = db.Column(db.String, nullable=False)
    year_of_estab = db.Column(db.Integer, nullable=False)
    annual_turnover = db.Column(db.Integer, nullable=False)
    employee_strength = db.Column(db.Integer, nullable=False)

    poc_1_name = db.Column(db.String, nullable=False)
    poc_1_contact_number = db.Column(db.Integer, nullable=False)
    poc_1_email = db.Column(db.String, unique = True)
    poc_1_designation = db.Column(db.String, nullable=False)

    poc_2_name = db.Column(db.String, nullable=False)
    poc_2_contact_number = db.Column(db.Integer, nullable=False)
    poc_2_email = db.Column(db.String, unique = True)
    poc_2_designation = db.Column(db.String, nullable=False)
