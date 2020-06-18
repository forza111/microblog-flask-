from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
'''name -переменная, переданная в класс Flask, является предопределенной переменной
Python, которая задается именем модуля, в котором она используется'''
app.config.from_object(Config)
'''Flask читает фаил конфигурации и применяет'''
db = SQLAlchemy(app)#объект db представляет БД
migrate = Migrate(app,db)#объект, который представит механизм миграции
login = LoginManager(app)
login.login_view = 'login'
'''значение login-именем функции(конечной точкой) для входа в систему. Другими словами имя,которое
вы будете использовать в вызове url_for, чтобы получить url'''

from app import routes,models