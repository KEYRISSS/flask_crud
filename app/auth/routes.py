from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm
from extensions import db

# ---------------- LOGIN ----------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))  # si ya está logueado, va a la lista de juegos

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=False)  # nunca recordar sesión
            flash(f'Bienvenido {user.username}', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('juegos'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html', form=form)

# ---------------- REGISTER ----------------
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('juegos'))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('El nombre de usuario ya existe', 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=form.username.data)
        user.password = form.password.data  # se asume que en el modelo se encripta
        db.session.add(user)
        db.session.commit()

        flash('Usuario registrado correctamente. Inicia sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

# ---------------- LOGOUT ----------------
@auth.route('/logout')
@login_required
def logout():
    logout_user()  # cierra sesión
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('auth.login'))  # redirige al login