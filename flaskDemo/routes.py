import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, SearchForm,UpdateAccountForm, VehicleForm, LocationForm
from flaskDemo.models import Customer, Vehicle, Reservation, Location, Brand, Trim, Style, Model
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy import or_
from sqlalchemy import and_
from decimal import *
from flask import Markup

@app.route("/")
def entry():
    return render_template('entry.html', title='entry')

@app.route("/home", methods=['GET','POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('list'))
    return render_template('home.html', title='home', form=form)

@app.route("/list", methods=['POST'])
def list():
    form = SearchForm()
    Pickup = form.Pickingup.data
    Dropoff = form.Dropoff.data
    Pickupdate = form.Pickupdate.data
    Pickuptime = form.Pickuptime.data
    Dropoffdate = form.Dropoffdate.data
    Dropofftime = form.Dropofftime.data
    dateTo = datetime.strptime("{} {}".format(Pickupdate, Pickuptime), "%Y-%m-%d %H:%M:%S")
    dateFrom = datetime.strptime("{} {}".format(Dropoffdate,Dropofftime), "%Y-%m-%d %H:%M:%S")
    if(dateTo < datetime.now()):

        flash('The Pickup date can not be in the past. Please check the Pickup date', 'danger')
        return redirect(url_for('home'))
    if(dateFrom < datetime.now()):
        flash('The Dropoff date can not be in the past. Please check the Dropoff date', 'danger')
        return redirect(url_for('home'))
    if(dateFrom <= dateTo):
        flash('The Dropoff date can not be before the Pickup date. Please check the Dropoff date', 'danger')
        flash('Pickup date should be today date or later', 'danger')
        return redirect(url_for('home'))
    if(dateFrom < datetime.now()):
        flash('Dropoff date should be today date or later', 'danger')
        return redirect(url_for('home'))
    if(dateFrom <= dateTo):
        flash('Pickup date should be less than or equal to Dropoff date', 'danger')

        return redirect(url_for('home'))
    results = Vehicle.query.join(Location,Vehicle.locationID == Location.locationID) \
    .join(Reservation,Vehicle.vehicleID == Reservation.vehicleID)\
    .filter(Reservation.pickupLocation == Pickup)\
    .filter(or_(and_(dateTo < Reservation.dateFrom,dateFrom < Reservation.dateFrom),and_(dateTo > Reservation.dateTo,dateFrom > Reservation.dateTo)))\
    .add_columns(Vehicle.style, Vehicle.BrandName, Vehicle.rate, Vehicle.ModelName,Vehicle.trimLevel,Vehicle.vehicleID, Vehicle.Year, Vehicle.transmission)
    return render_template('list.html', title='Cars List', pickup=Pickup, Dropoff=Dropoff, dateTo=dateTo, dateFrom=dateFrom, results=results)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.is_authenticated and (current_user.admin != True):
        return redirect(url_for('home'))
    import mysql.connector
    from mysql.connector import Error
    ''' Connect to MySQL database '''
    try:
        conn = mysql.connector.connect(host='45.55.59.121',
                                           database='ASF',
                                           user='ASF',
                                           password='ASFASFASF')
        if conn.is_connected():
            cursor = conn.cursor()
        else:
            flash('problem')
        cursor.execute("SELECT reservation.pickupLocation, COUNT(reservation.pickupLocation) AS ReservedLocationFrequency FROM reservation GROUP BY reservation.pickupLocation")
        row = cursor.fetchall()
    except Error as e:
        print(e)
    finally:
        conn.close()
    return render_template('admin.html', title='Adminstrator', row=row)





@app.route("/register", methods=['GET','POST'])
def register():
    vid = request.args.get('vid')
    pickup = request.args.get('pickup')
    dropoff = request.args.get('dropoff')
    dateFrom = request.args.get('dateFrom')
    dateTo = request.args.get('dateTo')
    dateT = datetime.strptime("{}".format(dateTo), "%Y-%m-%d %H:%M:%S")
    dateF = datetime.strptime("{}".format(dateFrom), "%Y-%m-%d %H:%M:%S")
    diff = abs((dateF - dateT).days)
    car = Vehicle.query.get_or_404(vid)
    amount = diff * car.rate
    tax = Decimal(amount) * Decimal(0.1)
    total = amount + tax
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        datetime.datetime.strptime("{}, {}".format(date, time), "%m-%d-%Y, %H:%M")
        """
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = Customer(username=form.username.data, email=form.email.data, password=hashed_password,fullName=form.fullname.data,phoneNumber=form.phonenumber.data)
        db.session.add(customer)
        db.session.commit()
        customer = Customer.query.filter_by(email=form.email.data).first()
        reservation = Reservation(customerID=customer.customerID, vehicleID=vid, dateFrom=dateFrom,dateTo=dateTo,pickupLocation=pickup,dropoffLocation=dropoff)
        db.session.add(reservation)
        db.session.commit()
        flash('Your car has been reserved and account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form, car=car, dateTo=dateTo, dateFrom=dateFrom, diff=diff, amount=amount, tax=tax, total=total)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer.admin and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin'))
        elif customer and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.city.data = current_user.city
    if current_user.image_file is None:
        image_file = Image.open('flaskDemo/default-img.jpg')
    else:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/vehicle/new", methods=['GET', 'POST'])
@login_required
def new_vehicle():
    if current_user.is_authenticated and (current_user.admin != True):
        return redirect(url_for('home'))

    form = VehicleForm()
    if form.validate_on_submit():
        loc = Location.query.get_or_404(form.locationName.data)
        veh = Vehicle(BrandName=form.BrandName.data, plateNumber=form.PlateNumber.data,ModelName=form.Model.data,Year=form.Year.data,style=form.Style.data,Transmission=form.transmission.data,TrimLevel=form.trimLevel.data,rate=form.Rate.data,locationID=loc.locationID)
        db.session.add(veh)
        db.session.commit()
        flash('You have added a new vehicle!', 'success')
        return redirect(url_for('admin'))
    return render_template('create_vehicle.html', title='New Vehicle',
                           form=form, legend='New Vehicle')


@app.route("/dept/new", methods=['GET', 'POST'])
@login_required
def new_dept():
    form = DeptForm()
    if form.validate_on_submit():
        dept = Department(dname=form.dname.data, dnumber=form.dnumber.data,mgr_ssn=form.mgr_ssn.data,mgr_start=form.mgr_start.data)
        db.session.add(dept)
        db.session.commit()
        flash('You have added a new department!', 'success')
        return redirect(url_for('home'))
    return render_template('create_dept.html', title='New Department',
                           form=form, legend='New Department')





@app.route("/loc/new", methods=['GET', 'POST'])
@login_required
def new_loc():
    if current_user.is_authenticated and (current_user.admin != True):
        return redirect(url_for('home'))
    form = LocationForm()
    if form.validate_on_submit():
        loc = Location(locationName=form.LocationName.data, city=form.City.data,state=form.State.data,zipcode=form.Zipcode.data)
        db.session.add(loc)
        db.session.commit()
        flash('You have added a new location!', 'success')
        return redirect(url_for('home'))
    return render_template('create_loc.html', title='New Location',
                           form=form, legend='New Location')


"""
@app.route("/dept/<dnumber>")
@login_required
def dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    return render_template('dept.html', title=dept.dname, dept=dept, now=datetime.utcnow())


@app.route("/dept/<dnumber>/update", methods=['GET', 'POST'])
@login_required
def update_dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    currentDept = dept.dname

    form = DeptUpdateForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentDept !=form.dname.data:
            dept.dname=form.dname.data
        dept.mgr_ssn=form.mgr_ssn.data
        dept.mgr_start=form.mgr_start.data
        db.session.commit()
        flash('Your department has been updated!', 'success')
        return redirect(url_for('dept', dnumber=dnumber))
    elif request.method == 'GET':
        form.dnumber.data = dept.dnumber   # notice that we ARE passing the dnumber to the form
        form.dname.data = dept.dname
        form.mgr_ssn.data = dept.mgr_ssn
        form.mgr_start.data = dept.mgr_start
    return render_template('update_dept.html', title='Update Department',
                           form=form, legend='Update Department')          # note the update template!




@app.route("/dept/<dnumber>/delete", methods=['POST'])
@login_required
def delete_dept(dnumber):
    dept = Department.query.get_or_404(dnumber)
    db.session.delete(dept)
    db.session.commit()
    flash('The department has been deleted!', 'success')
    return redirect(url_for('home'))
"""
