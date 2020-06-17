from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    '''Класс User наследует от db.model для всех моделей из FLASK_SQLAlchemy.
    Класс определяет несколько полей как экземпляры классы db.Column, который принимает
    тип поля в качестве аргумента + необязательный аргументы, которые позволяют указать
    какие поля уникальны и проиндексированы'''

    def __repr__(self):
        return '<User {}>'.format(self.username)
    '''сообщает Python,как печатать объекты этого класса, что будет полезно для отладки'''