from stakeholder import db

class GarmentAssembler(db.Model):
    __tablename__ = "garment_assembler"
    name_of_company = db.Column(db.String, unique=True, nullable=False)
    #TODO verify valid phone number
    contact_number = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, primary_key = True)
    password = db.Column(db.String, nullable=False)
    year_of_estab = db.Column(db.Integer, nullable=False)
    annual_turnover = db.Column(db.Integer, nullable=False)
    employee_strength = db.Column(db.Integer, nullable=False)

    fabrics_owned = db.relationship("InputFabric", backref = "garment_assembler")
    garments_produced = db.relationship("GarmentProduced", backref = "garment_assembler")
    transactions_with_retailer = db.relationship("TransactionWithRetailer", backref = "garment_assembler")

    poc_1_name = db.Column(db.String, nullable=False)
    poc_1_contact_number = db.Column(db.Integer, nullable=False)
    poc_1_email = db.Column(db.String, unique = True)
    poc_1_designation = db.Column(db.String, nullable=False)

class InputFabric(db.Model):
    __tablename__ = "input_fabric"
    rowid = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction_with_garment_assembler.rowid'), nullable = False)
    fabric = db.relationship("TransactionWithGarmentAssembler", foreign_keys=[transaction_id])
    weight_usable = db.Column(db.Float)
    owner = db.Column(db.String, db.ForeignKey("garment_assembler.email"))

class GarmentProduced(db.Model):
    __tablename__ = "garment_produced"
    rowid = db.Column(db.Integer, primary_key=True)
    producer = db.Column(db.String, db.ForeignKey("garment_assembler.email"))
    garment_name = db.Column(db.String, nullable = False)
    number_fabrics_used = db.Column(db.Integer, nullable = False)
    fabric1_id = db.Column(db.Integer, db.ForeignKey('input_fabric.rowid'), nullable = False)
    fabric1 = db.relationship("InputFabric", foreign_keys=[fabric1_id])
    fabric1_weight_used = db.Column(db.Float, nullable = False)
    fabric1_weight_wasted = db.Column(db.Float, nullable = False)

    fabric2_id = db.Column(db.Integer, db.ForeignKey('input_fabric.rowid'), nullable = False)
    fabric2 = db.relationship("InputFabric", foreign_keys=[fabric2_id])
    fabric2_weight_used = db.Column(db.Float, nullable = False)
    fabric2_weight_wasted = db.Column(db.Float, nullable = False)

    trimming_technique = db.Column(db.String, nullable = False)
    sewing_technique = db.Column(db.String, nullable = False)
    printing_technique = db.Column(db.String, nullable = False)
    chemical_finish = db.Column(db.String, nullable = False)
    screen_printing_or_heat_transfer = db.Column(db.Boolean, nullable = False)

    quantity_produced = db.Column(db.Integer, nullable = False)
    quantity_in_inventory = db.Column(db.Integer, nullable = False)
    production_cost_per_unit = db.Column(db.Float, nullable = False)

class TransactionWithRetailer(db.Model):
    __tablename__ = "transaction_with_retailer"
    rowid = db.Column(db.Integer, primary_key=True)
    garment_id = db.Column(db.Integer, db.ForeignKey('garment_produced.rowid'), nullable = False)
    garment = db.relationship("GarmentProduced", foreign_keys=[garment_id])
    quantity_sold = db.Column(db.Integer, nullable = False)
    sold_by = db.Column(db.Integer, db.ForeignKey('garment_assembler.email'), nullable = False)
    sold_to = db.Column(db.Integer, db.ForeignKey('retailer.email'), nullable = False)
    selling_price_per_unit = db.Column(db.Float, nullable = False)
    rebate = db.Column(db.Float, nullable = False)