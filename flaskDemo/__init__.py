from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://ASF:ASFASFASF@45.55.59.121/ASF"

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'smlgbr@gmail.com'  # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = 'smlgbr@gmail.com' # enter your email here
app.config['MAIL_PASSWORD'] = 'samuel471152' # enter your password here

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskDemo import routes
from flaskDemo import models

models.db.create_all()
