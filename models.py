from flask import flash, session
from sqlalchemy.sql import func
from config import db, bcrypt, migrate
from datetime import datetime

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    # Password requires 8-16 characters length, capital and lowercase letters, and special characters.
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$^+=!*()@%&]).{8,16}$')

favorites = db.Table("favorites",
            db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
            db.Column("pizza_id", db.Integer, db.ForeignKey("pizzas.id"), primary_key=True))

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(65))
    password = db.Column(db.String(255))
    street_address = db.Column(db.String(255))
    city = db.Column(db.String(80))
    state = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    pizzas_liked = db.relationship("Pizzas", secondary=favorites)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

        # REGISTRATION VALIDATIONS
    @classmethod
    def validate_registration(cls, user_info):
        is_valid = True
        if len(user_info['name']) < 1:
            is_valid = False
            flash('Please enter your name.', 'danger')
        if len(user_info['alias']) < 1:
            is_valid = False
            flash('Please enter an alias.', 'danger')
        elif len(user_info['alias']) > 0:
            for user in cls.query.all():
                if user.alias == user_info['alias']:
                    is_valid = False
                    flash('Alias already exists.', 'info')
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

class Pizzas(db.Model):
    __tablename__ = "pizzas"
    id = db.Column(db.Integer, primary_key=True)
    crust = db.Column(db.Integer, db.ForeignKey("crusts.id"), nullable=False)
    topping = db.Column(db.Integer, db.ForeignKey("toppings.id"), nullable=False)
    users_who_like = db.relationship("Users", secondary=favorites)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

class Crusts(db.Model):
    __tablename__ = "crusts"
    id = db.Column(db.Integer, primary_key=True)
    crust_type = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

class Toppings(db.Model):
    __tablename__ = "toppings"
    id = db.Column(db.Integer, primary_key=True)
    topping_type = db.Column(db.String(30))
    price = db.Column(db.Decimal)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

class States(db.Model):
    __tablename__ = "states"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())