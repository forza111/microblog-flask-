from flask import Flask
from config import Config

app = Flask(__name__)
'''name -переменная, переданная в класс Flask, является предопределенной переменной
Python, которая задается именем модуля, в котором она используется'''
app.config.from_object(Config)
'''Flask читает фаил конфигурации и применяет'''

from app import routes