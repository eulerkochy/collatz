from flask import Flask, render_template, abort
from flask import session, redirect, url_for
from stakeholder import db, app
from user import User
from fabric_manufacturer import FabricManufacturer, FabricProduced, RawFibre
from garment_assembler import GarmentAssembler
from retailer import Retailer
from forms import SignUpForm, LoginForm, SignUpUserForm, FibreForm
import json

db.drop_all()
db.create_all() 

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        stakeholder_type = form.stakeholder_type.data
        if stakeholder_type == "Fabric Manufacturer":
            Company  = FabricManufacturer
        elif stakeholder_type == "Garment Assembler":
            Company = GarmentAssembler
        else:
            Company = Retailer
        new_user = Company(
            name_of_company = form.name_of_company.data,
            state = form.state.data,
            city = form.city.data,
            contact_number = form.contact_number.data, #TODO verify valid phone number 
            address = form.address.data,
            email = form.email.data,
            password = form.password.data,
            year_of_estab = form.year_of_estab.data,
            annual_turnover = form.annual_turnover.data,
            employee_strength = form.employee_strength.data,
            poc_1_name = form.poc1_name.data,
            poc_1_contact_number = form.poc1_contact_number.data,
            poc_1_email = form.poc1_email.data,
            poc_1_designation = form.poc1_designation.data,
            poc_2_name = form.poc1_name.data,
            poc_2_contact_number = form.poc1_contact_number.data,
            poc_2_email = form.poc1_email.data,
            poc_2_designation = form.poc1_designation.data
        )
            
        db.session.add(new_user)
        
        if User.query.filter_by(email = form.email.data).first():
            return render_template("signup_user.html", form = form, message = "This Email already exists in the system! Please Login instead.")


        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form = form, message = "Error.")
        finally:
            db.session.close()
        return render_template("signup.html", message = "Successfully signed up")
    elif form.errors:
        print(form.errors.items())
    return render_template("signup.html", form = form)



@app.route("/signup_user", methods=["POST", "GET"])
def signup_user():
    form = SignUpUserForm()
    if form.validate_on_submit():
        new_user = User(
            name = form.name.data,
            email = form.email.data,
            contact_number = form.contact_number.data,
            password = form.password.data,
        )

        if User.query.filter_by(email = form.email.data).first():
            return render_template("signup_user.html", form = form, message = "This Email already exists in the system! Please Login instead.")

        db.session.add(new_user)
            
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup_user.html", form = form, message = "Error.")
        finally:
            db.session.close()
        print(User.query.all())

        return render_template("signup_user.html", message = "Successfully signed up")
    elif form.errors:
        print(form.errors.items())
    return render_template("signup_user.html", form = form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        stakeholder_type = form.type.data
        if stakeholder_type == "User":
            table = User
        elif stakeholder_type == "Fabric Manufacturer":
            table  = FabricManufacturer
        elif stakeholder_type == "Garment Assembler":
            table = GarmentAssembler
        else:
            table = Retailer
        
        user = table.query.filter_by(email = form.email.data).first()
        print(user)
        
        if user is None:
            return render_template("login.html", form = form, message = "Email id not registered")
        elif user.password != form.password.data:
            return render_template("login.html", form = form, message = "Incorrect password")
        else:
            session['user'] = user.email
            return render_template("login.html", message = "Successfully Logged In!")
    elif form.errors:
        print(form.errors.items())
    return render_template("login.html", form = form)

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home', _scheme='http', _external=True))

@app.route('/add_fibre', methods = ['POST', 'GET'])
def add_fibre():
    form = FibreForm()
    if form.validate_on_submit():
        new_fibre = RawFibre(
            source_location = form.source_location.data,
            manufacturer = form.manufacturer.data,
            contact_of_manufacturer = form.contact_of_manufacturer.data,
            fibre = form.fibre.data,
            weight = form.weight.data,
            weight_usable = form.weight.data,
            cost_per_unit = form.cost_per_unit.data,
            rebate = form.rebate.data,
            type_of_fibre = form.type_of_fibre.data,
            owner = session['user']
        )

        db.session.add(new_fibre)

        print(session['user'])
        user_in_session = FabricManufacturer.query.get(session['user'])
        user_in_session.fibres_owned.append(new_fibre)

            
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("add_fibre.html", form = form, message = "Error.")
        finally:
            db.session.close()

        return render_template("add_fibre.html", message = "Successfully added fibre")
    elif form.errors:
        print(form.errors.items())
    return render_template("add_fibre.html", form = form)

@app.route('/fibres_list')
def fibres_list():
    user_in_session = FabricManufacturer.query.get(session['user'])
    fibres = user_in_session.fibres_owned
    owner_company = user_in_session.name_of_company
    return render_template("fibres_list.html", fibres = fibres, owner_company = owner_company)

# def add_fabric():
#     user_in_session = RawFibre.query.get(session['user'])
#     form = FabricProducedForm(user_in_session)
#     fibres = user_in_session.fibres_owned

#     if form.validate_on_submit():
#         new_fabric = ()

#         db.session.add(new_fabric)

#         new_fabric.number_fibres_used = form.number_fibres_used.data
#         fibres_used = form.fibres_used.data #list of (fibre, manufacturer, id) values

#         quantities_used = []

#         for qty in form.quantities_in_order.data:
#             quantities_used.append(qty)

#         corresponding_quantity = {}
#         for fibre_data, qty in zip(fibres_used, quantities_used):
#             for f in fibres:
#                 if f.rowid == fibre_data[2]:
#                     if f.weight - qty >=0:
#                         f.weight_usable = fibres = user_in_session.fibres_owned
#                     else:
#                         db.session.rollback()
#                         return render_template("add_fabric.html", form = form, message = "Quantity larger than that in inventory")
#             corresponding_quantity[ fibre_data[0] ] = qty #{fibre: qty}       

#         print(fibres_used, quantities_used)

#         new_fabric.length_of_fabric = form.length_of_fabric.data

#         try:
#             db.session.commit()
#         except Exception as e:
#             print(e)
#             db.session.rollback()
#             return render_template("add_fabric.html", form = form, message = "Error.")
#         finally:
#             db.session.close()

#         return render_template("add_fabric.html", message = "Successfully added fabric")

#     elif form.errors:
#         print(form.errors.items())
#     return render_template("add_fabric.html", form = form)


if __name__ == "__main__":
    app.run(debug = True)
