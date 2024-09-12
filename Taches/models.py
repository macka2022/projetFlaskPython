from Taches import db, login_manager
from Taches import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# creation d'une class @User pour stocker les utilisateurs:
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(length=60), nullable=False, unique=True)
    email_address = db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    tasks = db.relationship('Task', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, password_lisible):
        self.password_hash = bcrypt.generate_password_hash(password_lisible).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)






# Creation d'une class @task pour stocker les donnees :
class Task(db.Model):

    __tablename__ = 'tasks'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    titre = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String(length=255))
    echeance = db.Column(db.Date())
    owner = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Tache {self.id} : {self.titre}"