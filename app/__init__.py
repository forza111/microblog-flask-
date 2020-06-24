from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)
'''name -переменная, переданная в класс Flask, является предопределенной переменной
Python, которая задается именем модуля, в котором она используется'''
app.config.from_object(Config)
'''Flask читает фаил конфигурации и применяет'''
db = SQLAlchemy(app)#объект db представляет БД
migrate = Migrate(app,db)#объект, который представит механизм миграции
login = LoginManager(app)
login.login_view = 'login'
'''значение login-является именем функции(конечной точкой) для входа в систему. Другими словами имя,
которое вы будете использовать в вызове url_for, чтобы получить url'''

if not app.debug:#вкл. регистратор эл. почты только, когда прил. работает без режима отладки
    if app.config['MAIL_SERVER']:#когда сервер эл. почты сущ. в конфигурации
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'],app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'],subject='Microblog Failure',
            credentials= auth,secure = secure
        )
        mail_handler.setLevel(logging.ERROR)#чтобы отправлял только сообщения об ошибках
        app.logger.addHandler(mail_handler)#прикреплял их к app.logger из FLASK




from app import routes,models,errors