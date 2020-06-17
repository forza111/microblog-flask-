from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
'''name -переменная, переданная в класс Flask, является предопределенной переменной
Python, которая задается именем модуля, в котором она используется'''
app.config.from_object(Config)
'''Flask читает фаил конфигурации и применяет'''
db = SQLAlchemy(app)#объект db представляет БД
migrate = Migrate(app,db)#объект, который представит механизм миграции


from app import routes,models