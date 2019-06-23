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
        return redirect("/main")
    else:
        return redirect("/")

def login():
    is_valid = Users.validate_registration(request.form)
    if is_valid:
        return redirect("/main")
    else:
        return redirect("/")

# Main Page

def main():
    if "userid" in session:
        current_user = Users.query.get(int(session['userid']))
        return render_template("main.html", user=current_user)
    else:
        return redirect("/")