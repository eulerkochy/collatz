from stakeholder import db

class User(db.Model):
    rowid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable= False)
    contact_number = db.Column(db.Integer, unique = True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String, nullable=False)