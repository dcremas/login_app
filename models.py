from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password_hashed = db.Column(db.String(128), default='')
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"Username: {self.username}, Email: {self.email}"

    def set_password(self, password):
        self.password_hashed = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hashed, password)
