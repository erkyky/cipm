import flask
import sqlite3
import flask.ext.login as login
import flask.ext.bootstrap as bs
from flask.ext.moment import Moment

app = flask.Flask(__name__)
app.config.from_object('config')

login_manager = login.LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

bootstrap = bs.Bootstrap()
moment = Moment()

login_manager.init_app(app)
bootstrap.init_app(app)
moment.init_app(app)


def get_db():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = flask.g._database = sqlite3.connect('cipm.db')
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

from cipm import views
