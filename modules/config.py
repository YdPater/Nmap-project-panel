from os.path import join, dirname, abspath
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# Create a login manager object
login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = abspath(dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + join(basedir, 'database', 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
static_path = join(basedir, 'static')
app.config['UPLOAD_FOLDER'] = join(static_path, 'upload_dir')
app.config['OUTPUT_DIR'] = join(static_path, 'writedir')

db = SQLAlchemy(app)
Migrate(app,db)

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "login"
