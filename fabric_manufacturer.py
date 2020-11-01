from stakeholder import db

class FabricManufacturer(db.Model):
    name_of_company = db.Column(db.String, unique=True, nullable=False)
    #TODO verify valid phone number
    contact_number = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, primary_key = True)
    password = db.Column(db.String, nullable=False)
    year_of_estab = db.Column(db.Integer, nullable=False)
    annual_turnover = db.Column(db.Integer, nullable=False)
    employee_strength = db.Column(db.Integer, nullable=False)

    fibres_owned = db.relationship("RawFibre", backref = "fabric_manufacturer")
    fabrics_produced = db.relationship("FabricProduced", backref = "fabric_manufacturer")
    transactions_with_garment_assembler = db.relationship("TransactionWithGarmentAssembler", backref = "fabric_manufacturer")

    poc_1_name = db.Column(db.String, nullable=False)
    poc_1_contact_number = db.Column(db.Integer, nullable=False)
    poc_1_email = db.Column(db.String, unique = True)
    poc_1_designation = db.Column(db.String, nullable=False)

class RawFibre(db.Model):
    __tablename__ = "raw_fibre"
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
    # used_in_fabrics = db.relationship("FabricProduced", backref = "raw_fibre")
    owner = db.Column(db.String, db.ForeignKey("fabric_manufacturer.email"))
    
class FabricProduced(db.Model):
    __tablename__ = "fabric_produced"
    rowid = db.Column(db.Integer, primary_key=True)
    fabric_name = db.Column(db.String, nullable=False)
    producer = db.Column(db.String, db.ForeignKey("fabric_manufacturer.email"))
    number_fibres_used = db.Column(db.Integer, nullable = False)
    fibre1_id = db.Column(db.Integer, db.ForeignKey('raw_fibre.rowid'), nullable = False)
    fibre1 = db.relationship("RawFibre", foreign_keys=[fibre1_id])
    fibre1_weight_used = db.Column(db.Float, nullable = False)
    fibre1_weight_wasted = db.Column(db.Float, nullable = False)

    area = db.Column(db.Float, nullable = False)
    weight = db.Column(db.Float, nullable = False)
    weight_in_inventory = db.Column(db.Float, nullable = False)
    production_cost_per_unit = db.Column(db.Float)

class TransactionWithGarmentAssembler(db.Model):
    __tablename__ = "transaction_with_garment_assembler"
    rowid = db.Column(db.Integer, primary_key=True)
    fabric_id = db.Column(db.Integer, db.ForeignKey('fabric_produced.rowid'), nullable = False)
    fabric = db.relationship("FabricProduced", foreign_keys=[fabric_id])
    area = db.Column(db.Float, nullable = False)
    weight = db.Column(db.Float, nullable = False)
    sold_by = db.Column(db.Integer, db.ForeignKey('fabric_manufacturer.email'), nullable = False)
    sold_to = db.Column(db.Integer, db.ForeignKey('garment_assembler.email'), nullable = False)
    selling_price_per_unit = db.Column(db.Float, nullable = False)
    rebate = db.Column(db.Float, nullable = False)