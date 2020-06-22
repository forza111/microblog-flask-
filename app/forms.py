from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError,DataRequired,Email,EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    '''первый аргумент выступает как метка(описание)
    Validators используется для привязки к полям.DataRequired проверяет
    что поле не было отправлено пустым'''

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    '''Валидатор Email - гарантирует, что то, что пользователь вводит в этом поле точно Email '''
    password = PasswordField('Password',validators=[DataRequired()])
    password2=PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    '''Валидатор EqualTo проверяет что значение второго пароля идентично значению первого пароля'''
    submit = SubmitField('Register')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please user a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email addres')

    '''В этом случае я хочу убедиться, что имя пользователя и адрес электронной почты, введенные 
    пользователем, еще не находятся в базе данных, поэтому эти два метода выдают запросы к базе 
    данных, ожидая, что результатов не будет. В случае, если результат существует, ошибка проверки 
    инициируется вызовом ValidationError. Сообщение, включенное в качестве аргумента в исключение, 
    будет сообщением, которое будет отображаться рядом с полем для просмотра пользователем.'''