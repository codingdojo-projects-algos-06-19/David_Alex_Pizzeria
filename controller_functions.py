from flask import render_template, redirect, request, session
from config import db, migrate
from models import Users, Pizzas, Toppings

# Index, Login and Registration

def index():
    return render_template("index.html")

def registration_page():
    return render_template("register.html")

def register():
    is_valid = Users.validate_registration(request.form)
    if is_valid:
        Users.register_user(request.form)
        return redirect("/home")
    else:
        return redirect("/registration")

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
    if "userid" in session:
        is_valid = Users.update_validation(request.form)
        if is_valid:
            Users.update_user(request.form)
        return redirect("/account")
    else:
        return redirect("/")

# Order Page

def order():
    if "userid" in session:
        current_user = Users.query.get(int(session['userid']))
        all_toppings = Toppings.query.all()
        ordercount = session['ordercount']
        return render_template("order.html", user=current_user, toppings=all_toppings, ordercount=ordercount)
    else:
        return redirect("/")

def add_pizza(method=["POST"]):
    if "userid" in session:
        current_user = Users.query.get(int(session['userid']))
        Pizzas.add_pizza(request.form)
        return redirect("/order")
    else:
        return redirect("/")

# Admin Page
 
def admin():
    if "userid" in session:
        all_toppings = Toppings.query.all()
        return render_template("admin.html", toppings=all_toppings)
    else:
        return redirect("/")

def add_topping():
    Toppings.add_topping(request.form)
    return redirect("/admin")

def delete_topping(id):
    Toppings.delete_topping(id)
    return redirect("/admin")

# Logout

def logout():
    session.clear()
    return redirect("/")