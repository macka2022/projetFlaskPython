from Taches import app
from Taches.models import Task, User
from flask import render_template, redirect, url_for, flash,request
from Taches.forms import RegisterForm, AddTask, LoginForm
from Taches import db
from flask_login import login_user, logout_user, login_required ,current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/tasks")
@login_required
def tasks_page():
    items = Task.query.all()
    return render_template("tasks.html", data=items)


@app.route("/register", methods=['GET', 'POST'])
def register_page():

    formulaire = RegisterForm()
    if formulaire.validate_on_submit():

        new_user = User(username=formulaire.username.data,
                        email_address=formulaire.email_address.data,
                        password=formulaire.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Votre compte a ete cree avec succes, connectez-vous", category='info')
        return redirect(url_for('login_page'))

    # Verifions si il ya une erreur dans les donnees saisies par l'utilisateur
    if formulaire.errors != {}: # si le dictionnaire est vide alors il n'ya pas d'erreurs
        for err_msg in formulaire.errors.values():
            flash(f"Il y a une erreur de type : {err_msg}", category="danger")

    return render_template("register.html", form=formulaire)


# chemin vers la page de @ajout-tache:
@app.route("/addTask", methods=['GET', 'POST'])
def add_task():
    # Mise en page du formulaire d'ajout de tache:
    form = AddTask()

    # verification des donnees fournies
    if form.validate_on_submit():
        new_task = Task(titre=form.titre.data,
                        description=form.description.data,
                        echeance=form.date_fin.data,
                        owner=current_user.id)

    # creation de la tache dans la base de donnees:
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('tasks_page'))

    # Verification et lecture des erreurs :
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f"Il y a une erreur de type : {err_msg}")

    # Generation de la page d'ajout
    return render_template("addTask.html", form=form)


# Chemin vers la page de connexion:
@app.route("/login", methods=['GET', 'POST'])
def login_page():
    # Formulaire de connexion:
    form = LoginForm()
    if form.validate_on_submit():
        connecting_user = User.query.filter_by(username=form.username.data).first()
        if connecting_user and connecting_user.check_password(
                attempted_password=form.password.data):
            login_user(connecting_user)
            flash(f'Vous etes en ligne en tant que : {connecting_user.username}!', category="success")
            return redirect(url_for("tasks_page"))

        else:
            flash("Le nom d'utilisateur ou le mot de passe est incorrect", category='danger')
    return render_template("login.html", form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash('Vous etes deconncete !', category='info')
    return redirect(url_for("login_page"))
@app.route('/tasks/<int:id>')
def delete_task():
    if  request.form.method == 'POST':
        task_id=Task.query.filter_by(id_task=Task.id)
        task= Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
        else:
            return "La Tacha Non Trouvé"
    else:
        return render_template("tasks.html")


