from app import app, db
from app.models import Customer, Guitar
from app.forms import CustomerForm, GuitarForm
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import or_

# Home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

# Add customer page
@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        existing_customer = Customer.query.filter(or_(
            Customer.email == form.email.data,
            Customer.phone == form.phone.data
        )).first()
        
        if existing_customer:
            flash(f'Customer with the same email or phone number already exists', 'error')
            return redirect(url_for('add_customer'))
        
        customer = Customer(firstname=form.firstname.data,
                            lastname=form.lastname.data,
                            email=form.email.data,
                            phone=form.phone.data)
        db.session.add(customer)
        db.session.commit()
        flash(f'Customer added successfully', 'success')
        return redirect(url_for('add_guitar'))
    
    return render_template('add_customer.html', title='Add Customer', form=form)



# Create Repair job page
@app.route('/guitars/add', methods=['GET', 'POST'])
def add_guitar():
    form = GuitarForm()
    if form.validate_on_submit():
        guitar = Guitar(
            customer_id=form.customer_id.data,
            brand=form.brand.data,
            model=form.model.data,
            serial_number=form.serial_number.data,
            description=form.description.data,
            repair_status=form.repair_status.data
        )
        db.session.add(guitar)
        db.session.commit()
        flash('Repair Job Createded Successfully', 'success')
        return redirect(url_for('view_guitars'))    
    return render_template('add_guitar.html', title='Add Guitar', form=form)


# view repair jobs
@app.route('/guitars/view', methods=['GET', 'POST'])
def view_guitars():
    guitars = Guitar.query.all()
    return render_template('view_guitars.html', guitars=guitars)


# view customers
@app.route('/customers/view', methods=['GET', 'POST'])
def view_customers():
    customers = Customer.query.all()
    return render_template('view_customers.html', customers=customers)

# view guitars broken down by custommer
@app.route('/customers/view/<int:customer_id>', methods=['GET', 'POST'])
def view_customer_guitars(customer_id):
    guitars = Guitar.query.filter_by(customer_id=customer_id)
    return render_template('view_customer_guitars.html', guitars=guitars)