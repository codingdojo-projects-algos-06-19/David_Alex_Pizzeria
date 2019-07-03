from config import app
from controller_functions import index, register, login, home, registration_page, logout, account, order, update_user, add_pizza, admin, add_topping, delete_topping

app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=register, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/home", view_func=home)
app.add_url_rule("/registration", view_func=registration_page)
app.add_url_rule("/logout", view_func=logout)
app.add_url_rule("/account", view_func=account)
app.add_url_rule("/account/update", view_func=update_user, methods=["POST"])
app.add_url_rule("/order", view_func=order)
app.add_url_rule("/add_pizza", view_func=add_pizza, methods=["POST"])
app.add_url_rule("/admin", view_func=admin)
app.add_url_rule("/add_topping", view_func=add_topping, methods=["POST"])
app.add_url_rule("/delete_topping/<id>", view_func=delete_topping)
# app.add_url_rule("/order/random", view_func=random_pizza)