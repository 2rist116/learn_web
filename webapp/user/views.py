from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.db import db


blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    title = "Авторизация"
    login_form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            login_user(user)
            flash('Вы вошли на сайт')
            return redirect(url_for('news.index'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    form = RegistrationForm()
    title = "Регистрация"
    return render_template('registration.html',
                           page_title=title, form=form)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(url_for('user.register'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы разлогинились!')
    return redirect(url_for('news.index'))
