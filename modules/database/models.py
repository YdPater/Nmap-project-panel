from modules import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Projects(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(30), index=True)
    description = db.Column(db.String(200))
    creator = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, naam, description, creator):
        self.naam = naam
        self.description = description
        self.creator = creator


class Scandata(db.Model):
    __tablename__ = 'scandata'

    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(16))
    state = db.Column(db.String(10))
    port = db.Column(db.Integer)
    service = db.Column(db.String(30))
    product = db.Column(db.String(30))
    version = db.Column(db.String(20))
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    notes = db.Column(db.String(500))

    def __init__(self, target, state, port, service, product, version, project_id, notes):
        self.target = target
        self.state = state
        self.port = port
        self.service = service
        self.product = product
        self.version = version
        self.project_id = project_id
        self.notes = notes


class Invites(db.Model):
    __tablename__ = "invites"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    uid = db.Column(db.Integer)

    def __init__(self, project_id, uid):
        self.project_id = project_id
        self.uid = uid
