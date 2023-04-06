from app import db

# Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    guitars = db.relationship('Guitar', backref='customer', lazy=True)

    def __repr__(self):
        return f"Customer('{self.firstname}', '{self.lastname}', '{self.phone}', '{self.email}')"

# Guitar model
class Guitar(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    serial_number = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(250), nullable=False)
    repair_status = db.Column(db.String(50), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def __repr__(self):
        return f"Guitar('{self.brand}', '{self.model}', '{self.serial_number}', '{self.description}', '{self.repair_status}', '{self.customer_id}')"
