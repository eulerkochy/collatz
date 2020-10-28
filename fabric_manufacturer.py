from stakeholder import db

class FabricManufacturer(db.Model):
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

    fibres_owned = db.relationship("RawFibre", backref = "fabric_manufacturer")

    poc_1_name = db.Column(db.String, nullable=False)
    poc_1_contact_number = db.Column(db.Integer, nullable=False)
    poc_1_email = db.Column(db.String, unique = True)
    poc_1_designation = db.Column(db.String, nullable=False)

    poc_2_name = db.Column(db.String, nullable=False)
    poc_2_contact_number = db.Column(db.Integer, nullable=False)
    poc_2_email = db.Column(db.String, unique = True)
    poc_2_designation = db.Column(db.String, nullable=False)


class RawFibre(db.Model):
    rowid = db.Column(db.Integer, primary_key=True)
    source_location = db.Column(db.String, nullable = False)
    manufacturer = db.Column(db.String, nullable = False)
    contact_of_manufacturer = db.Column(db.String, nullable = False)
    fibre = db.Column(db.String, nullable = False)
    weight = db.Column(db.Float, nullable = False)
    weight_usable = db.Column(db.Float, nullable = False)
    cost_per_unit = db.Column(db.Float, nullable = False)
    rebate = db.Column(db.Float, nullable = False)
    type_of_fibre = db.Column(db.String, nullable = False)
    owner = db.Column(db.String, db.ForeignKey("fabric_manufacturer.email"))

    
class FabricProduced(db.Model):
    rowid = db.Column(db.Integer, primary_key=True)
    number_fibres_used = db.Column(db.Integer)
    fibres_used = db.Column(db.JSON)
    length_of_fabric = db.Column(db.Float)
