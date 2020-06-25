from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler,RotatingFileHandler
import os

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

        if not os.path.exists('logs'):
            os.mkdir('logs')
        '''Создаем каталог log,если его не существует'''
        file_handler = RotatingFileHandler('logs/microblog.log',maxBytes=10240,
                                           backupCount=10)
        '''Я пишу логфайл с именем microblog.log. 
        Класс RotatingFileHandler удобен, потому что он переписывает журналы, гарантируя, что файлы 
        журнала не будут слишком большими, если приложение работает в течение длительного времени. 
        В этом случае я ограничиваю размер логфайла 10 КБ, и храню последние десять файлов журнала в 
        качестве резервных копий.'''
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s : %(message)s [in %(pathname)s : %[lineno]d]'
        ))
        '''Класс logging.Formatter предоставляет настройку формата сообщений журнала. Поскольку эти 
        сообщения отправляются в файл, я хочу, чтобы они содержали как можно больше информации. Поэтому я 
        использую формат, который включает отметку времени, уровень ведения журнала,
        сообщение, исходный файл и номер строки, откуда возникла запись в журнале.'''
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')
        '''Чтобы сделать регистрацию более полезной, я также понижаю уровень ведения журнала до категории 
        INFO, как в регистраторе приложений, так и в обработчике файлов. Если вы не знакомы с категориями 
        ведения журнала, это DEBUG, INFO, WARNING,ERROR и CRITICAL в порядке возрастания степени тяжести.'''


from app import routes,models,errors