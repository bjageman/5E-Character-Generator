from passlib.apps import custom_app_context as pwd_context
from .users.models import User

def authenticate(username, password):
    user = User.query.filter_by(username = username).first()
    if user and user.verify_password(password):
        return user
