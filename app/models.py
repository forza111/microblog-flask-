from datetime import datetime
from app import db,login
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    '''Класс User наследует от db.model для всех моделей из FLASK_SQLAlchemy.
    Класс определяет несколько полей как экземпляры классы db.Column, который принимает
    тип поля в качестве аргумента + необязательный аргументы, которые позволяют указать
    какие поля уникальны и проиндексированы'''

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    '''retationship - высокоуровневое представление о взаимоотношениях между users и posts.

    Для отношения один ко многим(напр. один пользователь и много сообщений) поле relationship 
    определяется обычно на стороне "один" и используется как удобный способ получить доступ к 
    "многим" 

    Первый аргумент - Post указывает класс, который представляет сторону отношений "много"
    backref - определяет имя поля, которое будет добавлено
    lazy - определяет как будет выполняться запрос БД для связи'''

    def __repr__(self):
        return '<User {}>'.format(self.username)
    '''сообщает Python,как печатать объекты этого класса, что будет полезно для отладки'''

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    '''Поле timestamp будет  проиндексировано(сообщения в хронологическом порядке)'''
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    '''user_id - внешний ключ для user.id - значит оно ссылается на значение id из таблицы users'''

    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
'''идентификатор, которой flask-login переходит к функции в качестве аргумента ,будет 
строкой, поэтому для баз данных, использующих числовые идентификаторы, необходимо 
преобразовать строку в целое число, как вы видите выше int(id).'''