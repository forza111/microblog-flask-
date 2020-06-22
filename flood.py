from app import db
from app.models import User,Post

user = User.query.filter_by(username = 'susan').first_or_404()

print(user)