#Contains Models for DB to prevent clutter of Main program.
from datetime import datetime
from antisocial_media import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(16), nullable=False, unique=True)
	email = db.Column(db.String(80), nullable=False, unique=True)
	image_file = db.Column(db.String(20), nullable=False, default='boring.jpg')
	password = db.Column(db.String(60), nullable=False)
	hr_violations = db.Column(db.Integer,nullable=False, default=0)
	posts = db.relationship('Post',backref='author',lazy=True)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	def __repr__(self):
		return f"Post('{self.post_date}','{self.content}')"
