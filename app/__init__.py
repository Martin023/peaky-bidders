from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bidders.db'
app.config['SECRET_KEY'] = 'ed96823c766c274dc3bd19e0'
app.config['UPLOADED_PHOTOS_DEST'] = 'app/static/photos'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

from app import views
