from app import app, db
from app.models import Customer, Guitar
from app.forms import CustomerForm, GuitarForm
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import or_

# landing page
@app.route('/')
def index():
    return render_template('index.html', title='Index')

#home page
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

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

# edit customer
@app.route('/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = CustomerForm()
    if form.validate_on_submit():
        customer.firstname = form.firstname.data
        customer.lastname = form.lastname.data
        customer.email = form.email.data
        customer.phone = form.phone.data
        db.session.commit()
        flash('Customer Updated Successfully', 'success')
        return redirect(url_for('view_customers'))
    elif request.method == 'GET':
        form.firstname.data = customer.firstname
        form.lastname.data = customer.lastname
        form.email.data = customer.email
        form.phone.data = customer.phone
    return render_template('edit_customer.html', title='Edit Customer', form=form)

# delete customer
@app.route('/customers/delete/<int:customer_id>', methods=['GET', 'POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    # delete all guitars associated with customer
    if customer:
        for guitar in customer.guitars:
            db.session.delete(guitar)

        # delete customer
        db.session.delete(customer)
        db.session.commit()
        flash('Customer and associated repair jobs deleted Successfully', 'success')
    else:
        flash('Customer not found', 'error')
    return redirect(url_for('view_customers'))


# delete guitar
@app.route('/guitars/delete/<int:guitar_id>', methods=['GET', 'POST'])
def delete_guitar(guitar_id):
    guitar = Guitar.query.get_or_404(guitar_id)
    if guitar:
        db.session.delete(guitar)
        db.session.commit()
        flash('Job deleted Successfully', 'success')
    else:
        flash('Job not found', 'error')
    return redirect(url_for('view_guitars'))

# edit guitar
@app.route('/guitars/edit/<int:guitar_id>', methods=['GET', 'POST'])
def edit_guitar(guitar_id):
    guitar = Guitar.query.get_or_404(guitar_id)
    form = GuitarForm()
    if form.validate_on_submit():
        guitar.customer_id = form.customer_id.data
        guitar.brand = form.brand.data
        guitar.model = form.model.data
        guitar.serial_number = form.serial_number.data
        guitar.description = form.description.data
        guitar.repair_status = form.repair_status.data
        db.session.commit()
        flash('Repair Job Updated Successfully', 'success')
        return redirect(url_for('view_guitars'))
    elif request.method == 'GET':
        form.customer_id.data = guitar.customer_id
        form.brand.data = guitar.brand
        form.model.data = guitar.model
        form.serial_number.data = guitar.serial_number
        form.description.data = guitar.description
        form.repair_status.data = guitar.repair_status
    return render_template('edit_guitar.html', title='Edit Guitar', form=form)
    