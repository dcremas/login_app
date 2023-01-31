from flask import render_template, url_for, redirect, flash
from app import app, db, login_manager
from forms import UserForm, LoginForm
from models import User
from flask_login import current_user, login_user, logout_user, login_required

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    image_file = url_for('static', filename='disappointed.jpg')
    return render_template('index.html', image_file=image_file)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/accounts')
@login_required
def accounts():
    current_accounts = User.query.all()
    return render_template('accounts.html', users=current_accounts)
