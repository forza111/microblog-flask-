from app import db
from app.models import User,Post

u = User(username='susan',email = 'susan@example.com')
u.set_password('cat')
db.session.add(u)
db.session.commit()
print(u)