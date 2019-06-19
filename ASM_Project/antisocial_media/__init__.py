#Initialize Flask & SQL, then Import Forms
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#Set Configurations for Secret Key and Database (SqlAlchemy)
app.config['SECRET_KEY'] = '8675309JeNnY0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#Set Value for Database
db = SQLAlchemy(app)

#Allow for Encryption/Decryption
bcrypt = Bcrypt(app)

#Set Login Manager to allow user logins
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from antisocial_media import routes