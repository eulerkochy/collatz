from stakeholder import db

class Retailer(db.Model):
    name_of_company = db.Column(db.String, unique=True, nullable=False)
    #TODO verify valid phone number
    contact_number = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, primary_key = True)
    password = db.Column(db.String, nullable=False)
    year_of_estab = db.Column(db.Integer, nullable=False)
    annual_turnover = db.Column(db.Integer, nullable=False)
    employee_strength = db.Column(db.Integer, nullable=False)

    garments_owned = db.relationship("InputGarment", backref = "retailer")
    transactions_with_user = db.relationship("TransactionWithUser", backref = "retailer")

    poc_1_name = db.Column(db.String, nullable=False)
    poc_1_contact_number = db.Column(db.Integer, nullable=False)
    poc_1_email = db.Column(db.String, unique = True)
    poc_1_designation = db.Column(db.String, nullable=False)

class InputGarment(db.Model):
    __tablename__ = "input_garment"
    rowid = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction_with_retailer.rowid'), nullable = False)
    garment = db.relationship("TransactionWithRetailer", foreign_keys=[transaction_id])
    quantity_in_inventory = db.Column(db.Integer)
    owner = db.Column(db.String, db.ForeignKey("retailer.email"))

class TransactionWithUser(db.Model):
    rowid = db.Column(db.Integer, primary_key=True)
    date_of_purchase = db.Column(db.Date)
    sold_by = db.Column(db.Integer, db.ForeignKey('retailer.email'))
    sold_to = db.Column(db.Integer, db.ForeignKey('user.email'))
    garment_id = db.Column(db.Integer, db.ForeignKey('input_garment.rowid'), nullable = False)
    garment = db.relationship("InputGarment", foreign_keys=[garment_id])
    packaging_info = db.Column(db.String, nullable = False)
    quantity_sold = db.Column(db.Integer, nullable = False)
    selling_price_per_unit = db.Column(db.Float, nullable = False)
    send_back = db.Column(db.Boolean, nullable = False)
    send_back_after_months = db.Column(db.Integer)

    