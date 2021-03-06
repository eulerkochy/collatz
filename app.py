from flask import Flask, render_template, abort, request
from flask import session, redirect, url_for
from stakeholder import db, app
from user import User
from fabric_manufacturer import FabricManufacturer, RawFibre, FabricProduced, TransactionWithGarmentAssembler
from garment_assembler import GarmentAssembler, InputFabric, GarmentProduced, TransactionWithRetailer
from retailer import Retailer, InputGarment, TransactionWithUser
from forms import SignUpForm, LoginForm, SignUpUserForm, InputFibreForm, FabricProducedForm, TransactionWithGarmentAssemblerForm, GarmentProducedForm, TransactionWithRetailerForm, TransactionWithUserForm, InputForm, ConfirmInputForm
from datetime import date

db.drop_all()
db.create_all() 

new_user_g = GarmentAssembler(
    name_of_company = "g1",
    contact_number = 111, 
    address = "1",
    email = "g1@gmail.com",
    password = "g1",
    year_of_estab = 1991,
    annual_turnover = 1,
    employee_strength = 10,
    poc_1_name = "xyz",
    poc_1_contact_number = 112,
    poc_1_email = "1@gmail.com",
    poc_1_designation = 1,
)

new_user_f = FabricManufacturer(
    name_of_company = "f1",
    contact_number = 111, 
    address = "1",
    email = "f1@gmail.com",
    password = "f1",
    year_of_estab = 1991,
    annual_turnover = 1,
    employee_strength = 10,
    poc_1_name = "xyz",
    poc_1_contact_number = 112,
    poc_1_email = "1@gmail.com",
    poc_1_designation = 1,
)
new_user_r = Retailer(
    name_of_company = "r1",
    contact_number = 111, 
    address = "1",
    email = "r1@gmail.com",
    password = "r1",
    year_of_estab = 1991,
    annual_turnover = 1,
    employee_strength = 10,
    poc_1_name = "xyz",
    poc_1_contact_number = 112,
    poc_1_email = "1@gmail.com",
    poc_1_designation = 1,
)

new_user = User(
    name = "u1",
    email = "u1@gmail.com",
    contact_number = 111,
    password = "u1",
)

db.session.add(new_user_f)
db.session.add(new_user_g)
db.session.add(new_user_r)            
db.session.add(new_user)

new_fibre = RawFibre(
    source_location = "Maharashtra",
    manufacturer = "Cotton Plus",
    contact_of_manufacturer = "9783702110",
    fibre = "Cotton",
    weight = 10.0,
    weight_usable = 10.0,
    cost_per_unit = 1.0,
    rebate = 1.0,
    type_of_fibre = "Organic",
    owner = "f1@gmail.com",
)

db.session.add(new_fibre)
new_user_f.fibres_owned.append(new_fibre)

fabric1 = FabricProduced(
    fabric_name = "Pure Cotton",
    producer = "f1@gmail.com",
    number_fibres_used = 1,
    fibre1_id = 1,
    fibre1 = new_fibre,
    fibre1_weight_used = 2.0,
    fibre1_weight_wasted = 1.0,
    area = 10.0,
    weight = 10.0,
    weight_in_inventory = 10.0,
    production_cost_per_unit = 1.0,
)

fabric2 = FabricProduced(
    fabric_name = "Sustainable Cotton",
    producer = "f1@gmail.com",
    number_fibres_used = 1,
    fibre1_id = 1,
    fibre1 = new_fibre,
    fibre1_weight_used = 5.0,
    fibre1_weight_wasted = 1.0,
    area = 50.0,
    weight = 50.0,
    weight_in_inventory = 50.0,
    production_cost_per_unit = 1.0,
)

db.session.add(fabric1)
db.session.add(fabric2)

new_user_f.fabrics_produced.append(fabric1)
new_user_f.fabrics_produced.append(fabric1)

trans1 = TransactionWithGarmentAssembler(
    fabric_id = 1,
    fabric = fabric1,
    area = 2,
    weight = 2,
    sold_by = 1,
    sold_to = 1,
    selling_price_per_unit = 1,
    rebate = 1
)

trans2 = TransactionWithGarmentAssembler(
    fabric_id = 2,
    fabric = fabric2,
    area = 5,
    weight = 5,
    sold_by = 1,
    sold_to = 1,
    selling_price_per_unit = 1,
    rebate = 1
)

db.session.add(trans1)
db.session.add(trans2)

new_user_f.transactions_with_garment_assembler.append(trans1)
new_user_f.transactions_with_garment_assembler.append(trans2)


try:
    db.session.commit()
except Exception as e:
    print(e)
    db.session.rollback()
finally:
    db.session.close()

@app.route("/transaction_tables")
def transaction_tables():
    _form_garment = None
    _form_input_by_garment_assembler = None
    _form_retailer = None

    _form_input_by_retailer = None
    _form_user = None

    user_in_session = session['user']
    fabrics_owned = None
    garments_produced = None
    transactions_retailer = None
    garments_owned = None
    transactions_user = None
    user_garment = GarmentAssembler.query.get(user_in_session)
    user_retailer = Retailer.query.get(user_in_session)
    if user_garment:
        print(user_garment)
        _form_garment = GarmentProducedForm()
        _form_input_by_garment_assembler = InputForm()
        _form_retailer = TransactionWithRetailerForm()
        fabrics_owned = user_garment.fabrics_owned
        garments_produced = user_garment.garments_produced
        transactions_retailer = user_garment.transactions_with_retailer
        print(fabrics_owned, garments_produced, transactions_retailer)
    elif user_retailer:
        print(user_retailer)
        _form_input_by_retailer = InputForm()
        _form_user = TransactionWithUserForm()
        garments_owned = user_retailer.garments_owned
        transactions_user = user_retailer.transactions_with_user
        print(garments_owned, transaction_with_user)
    return render_template(
        "transaction.html",
        fabrics_owned = fabrics_owned,
        garments_produced = garments_produced,
        transactions_retailer = transactions_retailer,
        garments_owned = garments_owned,
        transactions_user = transactions_user,
        form_garment = _form_garment,
        form_input_by_garment_assembler = _form_input_by_garment_assembler,
        form_retailer = _form_retailer,
        form_input_by_retailer = _form_input_by_retailer,
        form_user = _form_user
    )


@app.route("/waste_statistic")
def waste_statistic():
    return render_template("waste_statistic.html")
@app.route("/")
def home():
    _form = SignUpForm()
    _form_login = LoginForm()
    return render_template("front-page.html", form_login=_form_login, form=_form)

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
        )
            
        db.session.add(new_user)
        
        if Company.query.filter_by(email = form.email.data).first():
            return render_template("front-page.html", form = form, message_signup = "This Email already exists in the system! Please Login instead.")


        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("front-page.html", form = form, message_signup = "Error.")
        finally:
            db.session.close()
        return render_template("index.html")
    elif form.errors:
        print(form.errors.items())
    return render_template("front-page.html", form = form)



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
    form_login = LoginForm()
    if form_login.validate_on_submit():
        stakeholder_type = form_login.type.data
        if stakeholder_type == "User":
            table = User
        elif stakeholder_type == "Fabric Manufacturer":
            table  = FabricManufacturer
        elif stakeholder_type == "Garment Assembler":
            table = GarmentAssembler
        else:
            table = Retailer
        
        user = table.query.filter_by(email = form_login.email.data).first()
        print(user)
        
        if user is None:
            return render_template("front-page.html", form_login = form_login, message_login = "Email id not registered")
        elif user.password != form_login.password.data:
            return render_template("front-page.html", form_login = form_login, message_login = "Incorrect password")
        else:
            session['user'] = user.email
            return redirect("/index")
    elif form_login.errors:
        print(form_login.errors.items())
    return render_template("front-page.html", form_login = form_login)

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect("/")

@app.route('/input_fibre', methods = ['POST', 'GET'])
def input_fibre():
    form = InputFibreForm()
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
        new_fibre_id = new_fibre.rowid

            
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("input_fibre.html", form = form, message = "Error.")
        finally:
            db.session.close()

        return render_template("input_fibre.html", message = "Successfully added fibre, id =" + str(new_fibre_id))
    elif form.errors:
        print(form.errors.items())
    return render_template("input_fibre.html", form = form)

@app.route('/fibres_list')
def fibres_list():
    user_in_session = FabricManufacturer.query.get(session['user'])
    fibres = user_in_session.fibres_owned
    owner_company = user_in_session.name_of_company
    return render_template("fibres_list.html", fibres = fibres, owner_company = owner_company)

@app.route('/fabric_produced', methods = ['POST', 'GET'])
def fabric_produced():
    user_in_session = FabricManufacturer.query.get(session['user'])
    form = FabricProducedForm()
    if form.validate_on_submit():
        new_fabric = FabricProduced(
            fabric_name = form.fabric_name.data,
            producer = session['user'],
            number_fibres_used = form.number_fibres_used.data,
            fibre1_id = form.fibre1_id.data,
            fibre1 = RawFibre.query.get(form.fibre1_id.data),
            fibre1_weight_used = form.fibre1_weight_used.data,
            fibre1_weight_wasted = form.fibre1_weight_wasted.data,
            area = form.area.data,
            weight = form.weight.data,
            weight_in_inventory = form.weight.data,
            production_cost_per_unit = form.production_cost_per_unit.data
        )
        fibre1 = new_fabric.fibre1
        if not fibre1:
            print("invalid fibre id")
            return render_template("fabric_produced.html", form = form, message = "Invalid fibre ID")
        elif fibre1.weight_usable < form.fibre1_weight_used.data:
            print("larger qty")
            return render_template("fabric_produced.html", form = form, message = "Quantity used larger than that in inventory")
        else:
            fibre1.weight_usable = fibre1.weight_usable - float(form.fibre1_weight_used.data)
        
        db.session.add(new_fabric)
        user_in_session.fabrics_produced.append(new_fabric)
        fabric_id = new_fabric.rowid
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("fabric_produced.html", form = form, message = "Error.")
        finally:
            db.session.close()

        return render_template("fabric_produced.html", message = "Successfully added fabric, id ="+str(fabric_id))

    elif form.errors:
        print(form.errors.items())
    return render_template("fabric_produced.html", form = form)

@app.route('/fabric_produced_list')
def fabric_produced_list():
    user_in_session = FabricManufacturer.query.get(session['user'])
    fabrics = user_in_session.fabrics_produced
    owner_company = user_in_session.name_of_company
    return render_template("fabric_produced_list.html", fabrics = fabrics, owner_company = owner_company)

@app.route('/transaction_with_garment_assembler', methods = ['POST', 'GET'])
def transaction_with_garment_assembler():
    user_in_session = FabricManufacturer.query.get(session['user'])
    form_garment = TransactionWithGarmentAssemblerForm()
    
    if form_garment.validate_on_submit():
        new_transaction = TransactionWithGarmentAssembler(
            fabric_id = form_garment.fabric_id.data,
            fabric = FabricProduced.query.get(form_garment.fabric_id.data),
            area = form_garment.area.data,
            weight = form_garment.weight.data,
            sold_by = session['user'],
            sold_to = form_garment.sold_to.data,
            selling_price_per_unit = form_garment.selling_price_per_unit.data,
            rebate = form_garment.rebate.data        
        )
        
        fabric = new_transaction.fabric
        if not fabric:
            return render_template("transaction.html", form = form_garment, message = "Invalid fabric ID")
        elif fabric.weight_in_inventory < form_garment.weight.data:
            return render_template("transaction.html", form = form_garment, message = "Quantity sold larger than that in inventory")
        else:
            fabric.weight_in_inventory -= float(form_garment.weight.data)
        
        db.session.add(new_transaction)
        user_in_session.transactions_with_garment_assembler.append(new_transaction)
        transaction_id = new_transaction.rowid
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("transaction.html", form = form_garment, message = "Error.")
        finally:
            db.session.close()

        return redirect("/transaction_tables")

    elif form_garment.errors:
        print(form_garment.errors.items())
    return render_template("transaction.html", form = form_garment)

@app.route('/transaction_with_garment_assembler_list')
def transaction_with_garment_assembler_list():
    user_in_session = FabricManufacturer.query.get(session['user'])
    transactions = user_in_session.transactions_with_garment_assembler
    owner_company = user_in_session.name_of_company
    return render_template("transaction_with_garment_assembler_list.html", transactions = transactions, owner_company = owner_company)

@app.route('/input_by_garment_assembler', methods = ['POST', 'GET'])
def input_by_garment_assembler():
    user_in_session = GarmentAssembler.query.get(session['user'])
    form = InputForm()
    if form.validate_on_submit():
        new_input_fabric = InputFabric(
            transaction_id = form.transaction_id.data,
            fabric = TransactionWithGarmentAssembler.query.get(form.transaction_id.data),
            owner = session['user']        
        )
        
        db.session.add(new_input_fabric)
        new_input_fabric.weight_usable = new_input_fabric.fabric.weight
        user_in_session.fabrics_owned.append(new_input_fabric)
        fabric_id = user_in_session.fabrics_owned[-1]

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("transaction.html", form_input_by_garment_assembler = form, message = "Error.")
        finally:
            db.session.close()

        return redirect("/transaction_tables")
        
    elif form.errors:
        print(form.errors.items())
    return render_template("transaction.html", form_input_by_garment_assembler = form)

@app.route('/fabrics_owned_list')
def fabrics_owned_list():
    user_in_session = GarmentAssembler.query.get(session['user'])
    fabrics = user_in_session.fabrics_owned
    owner_company = user_in_session.name_of_company
    return render_template("fabrics_owned_list.html", fabrics = fabrics, owner_company = owner_company)

# @app.route('/confirm_garment_assembler_transaction', methods = ['POST', 'GET'])
# def confirm_garment_assembler_transaction():
#     form = ConfirmInputForm()

#     if form.validate_on_submit():
#         if request.form.get('confirm'):
#             return render_template("index.html", message_confirmation = "Fabric successfully added.")
#         else:
#             user_in_session = GarmentAssembler.query.get(session['user'])
#             transaction = user_in_session.fabrics_owned.pop()
#             last_input_fabric = InputFabric.query.get(transaction.rowid)
#             db.session.delete(last_input_fabric)
#             seller_transaction_input = TransactionWithGarmentAssembler.query.get(transaction.fabric.rowid)
#             fabric = FabricProduced.query.get(seller_transaction_input.fabric_id)
#             fabric.weight_in_inventory += seller_transaction_input.weight
#             db.session.delete(seller_transaction_input)

#             try:
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()
#                 return render_template("index.html", form_confirm_by_garment_assembler = form, message = "Error.")
#             finally:
#                 db.session.close()
#             session['message'] = "Incorrect transaction information, contact seller"
#             return redirect("/index")
#     elif form.errors:
#         print(form.errors.items())
#     return render_template("index.html", form_confirm_by_garment_assembler = form)
    
@app.route('/garment_produced', methods = ['POST', 'GET'])
def garment_produced():
    user_in_session = GarmentAssembler.query.get(session['user'])
    form_garment = GarmentProducedForm()
    if form_garment.validate_on_submit():
        print("in garment produced")
        new_garment = GarmentProduced(
            producer = session['user'],
            garment_name = form_garment.garment_name.data,
            number_fabrics_used = form_garment.number_fabrics_used.data,
            fabric1_id = form_garment.fabric1_id.data,
            fabric1 = InputFabric.query.get(form_garment.fabric1_id.data),
            fabric1_weight_used = form_garment.fabric1_weight_used.data,
            fabric1_weight_wasted = form_garment.fabric1_weight_wasted.data,
            fabric2_id = form_garment.fabric2_id.data,
            fabric2 = InputFabric.query.get(form_garment.fabric2_id.data),
            fabric2_weight_used = form_garment.fabric2_weight_used.data,
            fabric2_weight_wasted = form_garment.fabric2_weight_wasted.data,
            trimming_technique = form_garment.trimming_technique.data,
            sewing_technique = form_garment.sewing_technique.data,
            printing_technique = form_garment.printing_technique.data,
            chemical_finish = form_garment.chemical_finish.data,
            screen_printing_or_heat_transfer = form_garment.screen_printing_or_heat_transfer.data,
            quantity_produced = form_garment.quantity_produced.data,
            quantity_in_inventory = form_garment.quantity_produced.data,
            production_cost_per_unit = form_garment.production_cost_per_unit.data
            
        )
        fabric1 = new_garment.fabric1
        fabric2 = new_garment.fabric2
        if not fabric1 or not fabric2:
            return render_template("transaction.html", form_garment = form_garment, message = "Invalid fabric ID")
        elif fabric1.weight_usable < form_garment.fabric1_weight_used.data or fabric2.weight_usable < form_garment.fabric2_weight_used.data:
            return render_template("transaction.html", form_garment = form_garment, message = "Quantity used larger than that in inventory")
        else:
            fabric1.weight_usable = fabric1.weight_usable - float(form_garment.fabric1_weight_used.data)
            fabric2.weight_usable = fabric2.weight_usable - float(form_garment.fabric2_weight_used.data)

        db.session.add(new_garment)
        user_in_session.garments_produced.append(new_garment)
        garment_id = new_garment.rowid
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("transaction.html", form_garment = form_garment, message = "Error.")
        finally:
            db.session.close()
        return redirect("/transaction_tables")

    elif form_garment.errors:
        print(form_garment.errors.items())
    return render_template("transaction.html", form_garment = form_garment)

@app.route('/index')
def index():    
    return render_template("index.html")

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")

@app.route('/garment_produced_list')
def garment_produced_list():
    user_in_session = GarmentAssembler.query.get(session['user'])
    garments = user_in_session.garments_produced
    owner_company = user_in_session.name_of_company
    return render_template("garment_produced_list.html", garments = garments, owner_company = owner_company)

@app.route('/transaction_with_retailer', methods = ['POST', 'GET'])
def transaction_with_retailer():
    user_in_session = GarmentAssembler.query.get(session['user'])
    form = TransactionWithRetailerForm()

    if form.validate_on_submit():
        new_transaction = TransactionWithRetailer(
            garment_id = form.garment_id.data,
            garment = GarmentProduced.query.get(form.garment_id.data),
            quantity_sold = form.quantity_sold.data,
            sold_by = session['user'],
            sold_to = form.sold_to.data,
            selling_price_per_unit = form.selling_price_per_unit.data,
            rebate = form.rebate.data
        )
        print(new_transaction)
        garment = new_transaction.garment
        if not garment:
            print("not garment")
            return render_template("transaction.html", form_retailer = form, message = "Invalid garment ID")
        elif garment.quantity_in_inventory < form.quantity_sold.data:
            return render_template("transaction.html", form_retailer = form, message = "Quantity sold larger than that in inventory")
        else:
            garment.quantity_in_inventory -= int(form.quantity_sold.data)
        
        db.session.add(new_transaction)
        user_in_session.transactions_with_retailer.append(new_transaction)
        transaction_id = new_transaction.rowid
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("transaction.html", form_retailer = form, message = "Error.")
        finally:
            db.session.close()

        return redirect("/transaction_tables")
    elif form.errors:
        print(form.errors.items())
    return render_template("index.html", form_retailer = form)

@app.route('/transaction_with_retailer_list')
def transaction_with_retailer_list():
    user_in_session = GarmentAssembler.query.get(session['user'])
    transactions = user_in_session.transactions_with_retailer
    owner_company = user_in_session.name_of_company
    return render_template("transaction_with_retailer_list.html", transactions = transactions, owner_company = owner_company)

@app.route('/input_by_retailer', methods = ['POST', 'GET'])
def input_by_retailer():
    user_in_session = Retailer.query.get(session['user'])
    form = InputForm()
    if form.validate_on_submit():
        new_input_garment = InputGarment(
            transaction_id = form.transaction_id.data,
            garment = TransactionWithRetailer.query.get(form.transaction_id.data),
            owner = session['user']        
        )
        
        db.session.add(new_input_garment)
        new_input_garment.quantity_in_inventory = new_input_garment.garment.quantity_sold
        user_in_session.garments_owned.append(new_input_garment)

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("transaction.html", form_input_by_retailer = form, message = "Error.")
        finally:
            db.session.close()

        form = ConfirmInputForm()
        user_in_session = Retailer.query.get(session['user'])
        garment = user_in_session.garments_owned[-1]
        return redirect("/transaction_tables")
        
    elif form.errors:
        print(form.errors.items())
    return render_template("transaction.html", form_input_by_retailer = form)

@app.route('/garments_owned_list')
def garments_owned_list():
    user_in_session = Retailer.query.get(session['user'])
    garments = user_in_session.garments_owned
    owner_company = user_in_session.name_of_company
    return render_template("garments_owned_list.html", garments = garments, owner_company = owner_company)

@app.route('/confirm_retailer_transaction', methods = ['POST', 'GET'])
def confirm_retailer_transaction():
    form = ConfirmInputForm()

    if form.validate_on_submit():
        if request.form.get('confirm'):
            return render_template("input_by_retailer.html", message = "Garment successfully added.")
        else:
            user_in_session = Retailer.query.get(session['user'])
            transaction = user_in_session.garments_owned.pop()
            last_input_garment = InputGarment.query.get(transaction.rowid)
            db.session.delete(last_input_garment)
            seller_transaction_input = TransactionWithRetailer.query.get(transaction.garment.rowid)
            garment = GarmentProduced.query.get(seller_transaction_input.garment_id)
            garment.quantity_in_inventory += seller_transaction_input.quantity_sold
            db.session.delete(seller_transaction_input)

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return render_template("input_by_retailer.html", form = form, message = "Error.")
            finally:
                db.session.close()
            return render_template("input_by_retailer.html", message = "Incorrect transaction information, contact seller")
    elif form.errors:
        print(form.errors.items())
    return render_template("confirm_retailer_transaction.html", form = form)

@app.route('/transaction_with_user', methods = ['POST', 'GET'])
def transaction_with_user():
    form = TransactionWithUserForm()
    user_in_session = Retailer.query.get(session['user'])
    if form.validate_on_submit():
        new_transaction = TransactionWithUser(
            sold_by = session['user'],
            sold_to = form.sold_to.data,
            garment_id = form.garment_id.data,
            garment = InputGarment.query.get(form.garment_id.data),
            packaging_info = form.packaging_info.data,
            quantity_sold = form.quantity_sold.data,
            selling_price_per_unit = form.selling_price_per_unit.data,
            send_back = form.send_back.data,
            send_back_after_months = form.send_back_after_months.data
        )

        today = date.today()
        new_transaction.date_of_purchase = today

        garment = new_transaction.garment
        if not garment:
            return render_template("transaction.html", form_user = form, message = "Invalid garment ID")
        elif garment.quantity_in_inventory < form.quantity_sold.data:
            return render_template("transaction.html", form_user = form, message = "Quantity sold larger than that in inventory")
        else:
            garment.quantity_in_inventory -= float(form.quantity_sold.data)
        
        user_in_session.transactions_with_user.append(new_transaction)
        
        db.session.add(new_transaction)

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("transaction.html", form_user = form, message = "Error.")
        finally:
            db.session.close()

        return redirect("/transaction_tables")
        
    elif form.errors:
        print(form.errors.items())
    return render_template("transaction.html", form_user = form)

@app.route('/transaction_with_user_list')
def transaction_with_user_list():
    user_in_session = Retailer.query.get(session['user'])
    transactions = user_in_session.transactions_with_user
    owner_company = user_in_session.name_of_company
    return render_template("transaction_with_user_list.html", transactions = transactions, owner_company = owner_company)


if __name__ == "__main__":
    app.run(debug = True)