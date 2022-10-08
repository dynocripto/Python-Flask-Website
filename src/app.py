from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        # if logged_user != None:
        #     if logged_user.password:
        #         return redirect(url_for('home'))
        #     else:
        #         flash("Invalid password...")
        #         return render_template('auth/login.html')
        # else:
        #     flash("User not found...")
        #     return render_template('auth/login.html')
        print(logged_user)
    else:
        return render_template('auth/login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        cur = db.connection.cursor()
        cur.execute('''INSERT INTO user (username, password, fullname) 
        VALUES (%s, %s, %s)''', (username, password, fullname))
        db.connection.commit()
        redirect(url_for('login'))
    return render_template('./auth/register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    #csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
