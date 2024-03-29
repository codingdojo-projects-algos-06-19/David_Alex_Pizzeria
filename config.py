from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "we server only the freshest pizzas delivered right to your door"

# replace localhost with server IP when we move to deploy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pizzeria.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)