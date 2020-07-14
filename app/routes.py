from flask import render_template,flash,redirect,url_for,request
from app import app,db
from app.forms import LoginForm,RegistrationForm, EditProfileForm,PostForm
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,Post
from werkzeug.urls import url_parse
from datetime import datetime




@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
"""декоратор before_request регистрирует декорированную функцию, которая должна быть выполнена 
непосредственно перед функцией просмотра.Это очень полезно, потому что теперь я могу вставить код, 
который я хочу выполнить перед любой функцией просмотра в приложении, и я могу использовать его в 
одном месте. Реализация просто проверяет, зарегистрирован ли current_user, и в этом случае устанавливает 
последнее поле в текущее время"""

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required#функция становится защищенной и не разрешает доступ к пользователям, которые не
# аутентифицированны
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now life!')
        return redirect(url_for('index'))
    posts = current_user.followed_posts().all()
    return render_template('index.html', title='Home Page', form=form, posts=posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:#current_us-Значение этой переменной может быть пользовательским
        #объектом из БД (который Flask-Login читает через обратный вызов загрузчика пользователя,
        #представленный выше), или специальный анонимный пользовательский объект, если пользователь
        # еще не входил в систему
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        '''Метод validate_on_submit делает весь процесс обработки. Если вы вызвали метод, когда форма будет 
        представлена пользователю (т.е. перед тем, как у пользователя будет возможность ввести туда данные), 
        то он вернет False, в таком случае вы знаете, что должны отрисовать шаблон.
        
        Если validate_on_submit вызывается вместе как часть запроса отправки формы, то он соберет все данные, 
        запустит любые валидаторы, прикрепленные к полям, и если все в порядке вернет True, что указывает на 
        валидность данных. Это означает, что данные безопасны для включения в приложение.
        
        Если как минимум одно поле не проходит валидацию, тогда функция вернет False и это снова вызовет 
        отрисовку формы перед пользователем, тем самым дав возможность исправить ошибки. .'''

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
        ''''''
        if not next_page or url_parse(next_page).netloc != '':
            '''Чтобы определить, является ли URL относительным или абсолютным, я анализирую его с помощью 
            функции url_parse() Werkzeug, а затем проверяю, установлен ли компонент netloc или нет.'''
            next_page=url_for('index')
        return redirect(next_page)
    return render_template('login.html',title = 'Sign In',form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Configurates, you are now a registred user!')
        return redirect(url_for('login'))
    '''Логика, выполняемая внутри условия if validate_on_submit(), создает нового пользователя с именем, 
    электронной почтой и паролем, записывает их в базу данных и затем перенаправляет запрос на вход, чтобы 
    пользователь мог войти в систему.'''
    return render_template('register.html',title = 'Register',form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    """first_or_404() работает так же как first, но если при отсутсвтии результатов возвращает ошибку 404"""
    posts = [
        {'author' : user, 'body' : 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user = user, posts = posts)

@app.route('/edit_profile', methods = ['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    '''дубликаты в форме профиля редактирования будут предотвращены в большинстве случаев.'''
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your  changes have been saved')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',title = 'Edit Profile',
                                                       form = form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/explore')
@login_required
def explore():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',title = 'Explore', posts = posts)