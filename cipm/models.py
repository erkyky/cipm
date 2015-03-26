import flask.ext.login as login
import cipm
import werkzeug.security as security
from . import login_manager


@login_manager.user_loader
def load_user(username):
    sql = 'SELECT * FROM users WHERE username = ?'
    cur = cipm.get_db().execute(sql, [username])
    user = cur.fetchone()

    return User(user[0], user[1], user[2]) if user else None


class User(login.UserMixin):

    def __init__(self, username, email, password_hash=None, password=None):
        self.id = username
        self.username = username
        if password_hash:
            self.password_hash = password_hash
        else:
            self.password = password
        self.email = email

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = security.generate_password_hash(password)

    def verify_password(self, password):
        return security.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username