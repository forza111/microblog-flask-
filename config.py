import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    '''Значение секретного ключа задается как выражение с двумя терминами, к которым
    присоединяется оператор or. Первый термин ищет значение переменной среды,также называемой
    SECRET_KEY, второй термин это просто жестко закодированная строка'''

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.dp')
    '''Расширение FLASK принимает местополож-ие БД приложение.
    Сначала берем URL-адрес БД.Если это не определено, настраивается БД с именем app.db,
    которая хранится в переменной basedir'''

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    '''отключаем функцию Flask_SQLALCHEMY, которая сигнализирует приложению каждый раз,
    когда в базе данных должно быть внесено изменение'''

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['pythonbyforza@gmail.com']

    POSTS_PER_PAGE = 30
    '''сколько элементов будет отображаться на странице'''