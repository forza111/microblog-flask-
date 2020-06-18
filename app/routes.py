from flask import render_template,flash,redirect,url_for,request
from app import app
from app.forms import LoginForm
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required#функция становится защищенной и не разрешает доступ к пользователям, которые не
# аутентифицированны
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
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:#current_us-Значение этой переменной может быть пользовательским
        #объектом из БД (который Flask-Login читает через обратный вызов загрузчика пользователя,
        #представленный выше), или специальный анонимный пользовательский объект, если пользователь
        # еще не входил в систему
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        '''результат функции filter_by- это запрос, который включает только объекты, у которых есть совпадающее
        имя польователя.Поскольку известно, что будет только один или нулевой результат,я завершу запрос,
        вызвав first(), который вернет объект пользователя,если он существует или None'''
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')#flash - фласк сохраняет сообщение, но на веб серверах не
            # будут появляться сообщения
            return redirect(url_for('login'))#функция указывает веб браузеру клиента автоматически
            # #перейти на другую страницу, указанную в качестве аргумента(/login)
        login_user(user,remember=form.remember_me.data)
        '''функция будет регестрировать пользователя во время входа в систему, поэтому это означает, что
        на любых будущих страницах, к которым пользователь переходит, будет установлена переменная 
        current_user для этого пользователя'''
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page=url_for('idex')
        return redirect(next_page)
    return render_template('login.html',title = 'Sign In',form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))