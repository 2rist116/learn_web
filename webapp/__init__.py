from flask import Flask, render_template, flash, redirect, url_for

from webapp.weather import weather_by_city
from webapp.model import News, db, User
from webapp.forms import LoginForm, RegistrationForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate

# set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        title = "Новости Python"
        weather = weather_by_city(app.config["WEATHER_DEFAULT_CITY"])
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)

    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('news.index'))
        form = RegistrationForm()
        title = "Регистрация"
        return render_template('user/registration.html',
                               page_title=title, form=form)

    @app.route('/process-reg', methods=['POST'])
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

    @app.route('/login')
    def login():
        title = "Авторизация"
        login_form = LoginForm()
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('index'))
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ'
        else:
            return 'Ты не админ!'
    return app
