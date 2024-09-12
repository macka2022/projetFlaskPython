from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from Taches.models import User


# Creation du Formulaire pour l'enregistrement des utilisateurs:
class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("This username already exist!")


    def validate_email(self, email_to_check):
        user_mail = User.query.filter_by(email_address=email_to_check.data).first()
        if user_mail:
            raise ValidationError('This email exist! ')

    username = StringField(label="Nom d'utlisateur :", validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address: ', validators=[Email(), DataRequired()])
    password = PasswordField(label='Mot de passe :', validators=[Length(min=5), DataRequired()])
    confirmPassword = PasswordField(label='Confirmer Mot de passe :', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Inscription')


# Formulaire pour la creation des Taches:
class AddTask(FlaskForm):
    titre = StringField(label="Nom de la tache :", validators=[Length(max=20), DataRequired()])
    description = StringField(label="Description :", validators=[Length(max=255)])
    date_fin = DateField(label="Echeance :", validators=[DataRequired()])
    submit = SubmitField(label='Ajouter')


# Formulaire de connexion utilisateurs:
class LoginForm(FlaskForm):
    username = StringField(label="Nom d'utilisateur :", validators=[DataRequired()])
    password = PasswordField(label="Mot De passe :", validators=[DataRequired()])
    submit = SubmitField(label='Se connecter')
