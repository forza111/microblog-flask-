from flask import render_template,flash,redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Эльдар Рязанов'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    '''аргумент methods - сообщение FLASK,что эта
#функция просмотра принимает запросы GET и POST(по умолчанию только GET)
#GET запросы - это те, что возвращают информацию клиенту(в этом случае веб браузер
#запросы POST обычно исп. когда браузер передает данные формы на сервер'''
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me {}'.format(
            form.username.data, form.remember_me.data))
        '''flash - фласк сохраняет сообщение, но на веб серверах не
        будут появляться сообщения'''
        return redirect('/index')
    '''функция указывает веб браузеру клиента автоматически
    перейти на другую страницу, указанную в качестве аргумента(/index)'''
    return render_template('login.html',title = 'Sign In',form = form)