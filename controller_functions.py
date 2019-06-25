from flask import render_template, redirect, request, session
from config import db, migrate
from models import Users, Pizzas, Crusts, Toppings, States

# Index, Login and Registration

def index():
    return render_template("index.html")

def registration_page():
    all_states = States.query.all()
    return render_template("register.html", states=all_states)

def register():
    is_valid = Users.validate_registration(request.form)
    if is_valid:
        Users.register_user(request.form)
        return redirect("/home")
    else:
        return redirect("/")

def login():
    is_valid = Users.validate_login(request.form)
    if is_valid:
        return redirect("/home")
    else:
        return redirect("/")

# Main Page

def home():
    if "userid" in session:
        current_user = Users.query.get(int(session['userid']))
        return render_template("home.html", user=current_user)
    else:
        return redirect("/")


# Account Page

def account():
    if "userid" in session:
        current_user = Users.query.get(int(session['userid']))
        return render_template("account.html", user=current_user)
    else:
        return redirect("/")

def update_user():
    if "userid" in session and Users.update_validation:
        Users.update_user(request.form)
        return redirect("/account")
    else:
        return redirect("/")

# Order Page

def order():
    if "userid" in session:
        current_user = Users.query.get(int(session['userid']))
        return render_template("order.html", user=current_user)
    else:
        return redirect("/")


# Logout

def logout():
    session.clear()
    return redirect("/")