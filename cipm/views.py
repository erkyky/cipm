import flask
import cipm
import cipm.forms as forms
import cipm.models as models
import datetime
import flask.ext.login as login_module
import werkzeug.security as security


@cipm.app.route('/secret')
@login_module.login_required
def secret():
    return 'Only authenticated users are allowed!'


@cipm.app.route('/', methods=['GET', 'POST'])
def index():
    return flask.render_template('index.html')


@cipm.app.route('/community')
def community():
    return flask.render_template('community.html')


@cipm.app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        db = cipm.get_db()
        conn = db.execute('SELECT * FROM users WHERE username = ?', [form.username.data])
        result = conn.fetchone()
        user = models.User(result[0], result[2], password_hash=result[1])
        if result is not None and user.verify_password(form.password.data):
            login_module.login_user(user, form.remember_me.data)
            return flask.redirect(flask.request.args.get('next') or flask.url_for('index'))
        flask.flash('Invalid username or password.')
    return flask.render_template('auth/login.html', form=form)


@cipm.app.route('/logout', methods=['GET'])
def logout():
    login_module.logout_user()
    flask.flash('You have been logged out.')
    return flask.redirect(flask.url_for('index'))


@cipm.app.route('/patientform', methods=['GET', 'POST'])
@login_module.login_required
def patientform():
    form = forms.PatientForm()
    if form.validate_on_submit():
        primary_issue = form.primary_issue.data
        if primary_issue == '0':
            is_emergency = form.chest_emergency.data
        if primary_issue == '1':
            is_emergency = form.breath_emergency.data
        if primary_issue == '2':
            is_emergency = form.weight_emergency.data
        if primary_issue == '3':
            is_emergency = form.medication_emergency.data
        if primary_issue == '4':
            is_emergency = str(form.bloodsugar_emergency.data)
        if primary_issue == '5':
            is_emergency = form.other_emergency.data

        if not is_emergency:
            # TODO fail somehow here
            pass

        username = login_module.current_user.username
        current_time = datetime.datetime.today()
        db = cipm.get_db()
        db.execute('INSERT INTO symptoms VALUES (?,?,?,?)', [username, primary_issue, is_emergency, current_time])
        db.commit()
        return flask.redirect('/thankyou')
    return flask.render_template('patientform.html', form=form)


@cipm.app.route('/halp')
def halp():
    db = cipm.get_db()
    conn = db.execute('SELECT * FROM symptoms')
    result = conn.fetchall()
    return flask.render_template('halp.html', symptoms=result)


@cipm.app.route('/thankyou')
def thankyou():
    return flask.render_template('thanksyou.html')


@cipm.app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        db = cipm.get_db()
        email = form.email.data
        username = form.username.data
        password = form.password.data
        password_hash = security.generate_password_hash(password)
        db.execute('INSERT INTO users VALUES (?,?,?)', [username, password_hash, email])
        db.commit()

        flask.flash('You can now login.')
        return flask.redirect(flask.url_for('login'))
    return flask.render_template('auth/register.html', form=form)
