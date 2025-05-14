from flask import Flask
from flask_mysqldb import MySQL
from config import SECRET_KEY, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST
from flask_bcrypt import Bcrypt

mysql = MySQL() #instancia do banco criada aqui
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'ef4e607f7f192b5607b45528925e59b3'
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MYSQL_HOST'] = MYSQL_HOST
    app.config['MYSQL_USER'] = MYSQL_USER
    app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
    app.config['MYSQL_DB'] = MYSQL_DB

    mysql.init_app(app)
    bcrypt.init_app(app)
# aqui vai iniciar o MySQL com o app


    from app.routes import main

    app.register_blueprint(main)
    return app

