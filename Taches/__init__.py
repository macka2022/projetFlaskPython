from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy  # sqlachemy permet de creer une mini database
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '70a23562112eecdddf71db37'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:passer@localhost:5433/exam'
# URI : Uniform Resources Identifier

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from Taches import routes
