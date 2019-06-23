from config import app
from controller_functions import index, register, login, main, registration_page

app.add_url_rule("/", viewfunc=index)
app.add_url_rule("/register", viewfunc=register, methods=["POST"])
app.add_url_rule("/login", viewfunc=login, methods=["POST"])
app.add_url_rule("/main", viewfunc=main)
app.add_url_rule("/registration", viewfunc=registration_page)