from flask import flash, session
from sqlalchemy.sql import func
from config import db, bcrypt, migrate
from datetime import datetime

import random
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    # Password requires 8-16 characters length, capital and lowercase letters, and special characters.
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$^+=!*()@%&]).{8,16}$')

favorites = db.Table("favorites",
            db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
            db.Column("pizza_id", db.Integer, db.ForeignKey("pizzas.id"), primary_key=True))

pizza_has_toppings = db.Table("pizza_has_toppings",
                     db.Column("pizza_id", db.Integer, db.ForeignKey("pizzas.id"), primary_key=True),
                     db.Column("topping_id", db.Integer, db.ForeignKey("toppings.id"), primary_key=True))

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(65))
    password = db.Column(db.String(255))
    street_address = db.Column(db.String(255))
    city = db.Column(db.String(80))
    state = db.Column(db.String(20))
    pizzas_liked = db.relationship("Pizzas", secondary=favorites)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

        # REGISTRATION VALIDATIONS
    @classmethod
    def validate_registration(cls, user_info):
        is_valid = True
        if len(user_info['first_name']) < 1:
            is_valid = False
            flash('Please enter your first name.', 'danger')
        if len(user_info['last_name']) < 1:
            is_valid = False
            flash('Please enter your last name.', 'danger')
        if len(user_info['email']) < 1:
            is_valid = False
            flash('Please enter an email address.', 'danger')
        elif not EMAIL_REGEX.match(user_info['email']):
            is_valid = False
            flash('Please enter a valid email address.', 'danger')
        elif EMAIL_REGEX.match(user_info['email']):
            for user in cls.query.all():
                if user.email == user_info['email']:
                    is_valid = False
                    flash('Email address already registered.', 'info')
        if len(user_info['password']) < 1:
            is_valid = False
            flash('Please enter a password', 'danger')
        elif not PASSWORD_REGEX.match(user_info['password']):
            is_valid = False
            flash('Password does not meet complexity requirements.', 'danger')
        elif user_info['password'] != user_info['confirm_password']:
            is_valid = False
            flash('Passwords do not match.', 'danger')
        if len(user_info['address']) < 6:
            is_valid = False
            flash('Please enter a valid street address.', 'danger')
        return is_valid

        # LOGIN VALIDATIONS
    @classmethod
    def validate_login(cls, user_info):
        is_valid = True
        match = 0
        if len(user_info['email']) < 1:
            is_valid=False
            flash("Please enter your email address.", "danger")
        elif len(user_info['password']) < 1:
            is_valid=False
            flash("Please enter your password.", "danger")
        elif not EMAIL_REGEX.match(user_info['email']):
            is_valid=False
            flash("Please enter a valid email address.", "danger")
        else:
            for user in cls.query.all():
                if user.email == user_info['email']:
                    match += 1
                    this_user = user
                    session['userid'] = user.id
                    session['order'] = []
                    session['ordercount'] = 0
            if match < 1:
                is_valid=False
                flash("Email address is not registered.", "danger")
            elif match > 0:
                if not bcrypt.check_password_hash(this_user.password, user_info['password']):
                    is_valid=False
                    flash("Incorrect username or password.", "danger")
        return is_valid

        # USER REGISTRATION
    @classmethod
    def register_user(cls, user_info):
        encrypted_pw = bcrypt.generate_password_hash(user_info['password'])
        new_user = cls(first_name=user_info['first_name'], last_name=user_info['last_name'], email=user_info['email'], password=encrypted_pw, street_address=user_info['address'], city=user_info['city'], state=user_info['state'])
        db.session.add(new_user)
        db.session.commit()
        for user in cls.query.all():
            if user.email == new_user.email:
                session['userid'] = user.id
                session['order'] = []
                session['ordercount'] = 0
    
        # UPDATE USER ACCOUNT VALIDATIONS
    @classmethod
    def update_validation(cls, user_info):
        is_valid = True
        current_user = cls.query.get(int(session['userid']))
        if len(user_info['first_name']) < 1:
            user_info['first_name'] = current_user.first_name
        if len(user_info['last_name']) < 1:
            user_info['last_name'] = current_user.last_name
        if len(user_info['email']) < 1:
            user_info['email'] = current_user.email
        if not EMAIL_REGEX.match(user_info['email']):
            is_valid = False
            flash('Please enter a valid email address.', 'danger')
        elif EMAIL_REGEX.match(user_info['email']):
            for user in cls.query.all():
                if user.email == user_info['email']:
                    is_valid = False
                    flash('Email address already registered.', 'info')
        if len(user_info['password']) < 1:
            is_valid = False
            flash('Please enter a new password.', 'danger')
        elif not PASSWORD_REGEX.match(user_info['password']):
            is_valid = False
            flash('Password does not meet complexity requirements.', 'danger')
        elif user_info['password'] != user_info['confirm_password']:
            is_valid = False
            flash('Passwords do not match.', 'danger')
        if len(user_info['address']) <1:
            user_info['address'] = current_user.street_address
        elif len(user_info['address']) < 6:
            is_valid = False
            flash('Please enter a valid street address.', 'danger')
        return is_valid

        # UPDATE USER ACCOUNT
    @classmethod
    def update_user(cls, user_info):
        current_user = cls.query.get(int(session['userid']))
        new_pass = bcrypt.generate_password_hash(user_info['password'])
        current_user.first_name = user_info['first_name']
        current_user.last_name = user_info['last_name']
        current_user.email = user_info['email']
        current_user.street_address = user_info['address']
        current_user.city = user_info['city']
        current_user.state = user_info['state']
        current_user.password = new_pass
        db.session.commit()
        flash("Account information has been updated!", "Success")

class Pizzas(db.Model):
    __tablename__ = "pizzas"
    id = db.Column(db.Integer, primary_key=True)
    crust = db.Column(db.String(14))
    users_who_like = db.relationship("Users", secondary=favorites)
    toppings = db.relationship("Toppings", secondary=pizza_has_toppings)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

# Add new pizza to order
    @classmethod
    def add_pizza(cls, user_info):
        current_user = Users.query.get(int(session['userid']))
        newPizza = cls(crust=user_info['crust'], topping=user_info.getlist('topping'))
        db.session.add(newPizza)
        db.session.commit()
        for pizza in cls.query.all():
            if pizza.crust == newPizza.crust and pizza.toppings == newPizza.toppings:
                pizza.users_who_like = session['userid']
                current_user.pizzas_liked = pizza.id
        session['order'] += newPizza
        session['ordercount'] += 1
        flash("Pizza added to cart!", "info")

# Create a random pizza
    # @classmethod
    # def random_pizza(cls):
    #     random_crust = Crust.query.get(random.randint(1,3))
    #     random_toppings = Toppings.query.get(random.randint(0,15))
    #     newPizza = cls(crust=random_crust)

class Toppings(db.Model):
    __tablename__ = "toppings"
    id = db.Column(db.Integer, primary_key=True)
    topping = db.Column(db.String(255))
    price = db.Column(db.Float)
    pizza = db.relationship("Pizzas", secondary=pizza_has_toppings)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    @classmethod
    def add_topping(cls, user_info):
        try:
            if len(user_info['topping']) > 1 and isinstance(float(user_info['price']), float):
                newTopping = cls(topping=user_info['topping'], price=float(user_info['price']))
                db.session.add(newTopping)
                db.session.commit()
                flash("Topping added!", "success")
            else:
                flash("Enter a valid topping.", "danger")
        except:
            flash("That's not a valid price.", "danger")
    @classmethod
    def delete_topping(cls, id):
        currentTopping = cls.query.get(id)
        db.session.delete(currentTopping)
        db.session.commit()
        flash("Topping deleted.", "info")