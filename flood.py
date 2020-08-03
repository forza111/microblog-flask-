from app import app
from flask_mail import Message
from app import mail


msg = Message('test subject', sender=app.config['ADMINS'][0],
recipients=['nikitos.ionkin111@gmail.com'])
msg.body = 'text body'
msg.html = '<h1>HTML body</h1>'

mail.send(msg)

