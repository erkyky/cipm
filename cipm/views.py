import flask
import cipm
import cipm.forms as forms
import cipm.models as models
import datetime
import dateutil.parser
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
        issue = form.primary_issue.data
        if issue == '0':
            details = form.chest_emergency.data
        elif issue == '1':
            details = form.breath_emergency.data
        elif issue == '2':
            details = '{a}lbs'.format(a=form.weight_emergency.data)
        elif issue == '3':
            details = form.medication_emergency.data
        elif issue == '4':
            details = '{a}mg/dL'.format(a=form.bloodsugar_emergency.data)
        elif issue == '5':
            details = form.fall_emergency.data
        elif issue == '99':
            details = form.other_emergency.data

        if not details:
            # TODO fail somehow here
            pass

        username = login_module.current_user.username
        current_time = datetime.datetime.today()

        db = cipm.get_db()
        db.execute('INSERT INTO symptoms VALUES (?,?,?,?,?)', [username, issue, details, form.extra.data, current_time])
        db.commit()
        return flask.redirect('/thankyou')
    return flask.render_template('patientform.html', form=form)


@cipm.app.route('/panel')
def panel():
    db = cipm.get_db()
    conn = db.execute('SELECT p.username, p.firstname, p.surname, s.symptom, s.details, s.extra, s.reported, p.city, '
                      'p.state, p.phone FROM symptoms s inner join passport p on s.username == p.username')
    results = conn.fetchall()

    symptoms = []
    severity_map = {'0': 'high', '1': 'high', '2': 'med', '3': 'med', '4': 'low', '5': 'low', '99': 'low'}
    severity_colors = {'high': 'red', 'med': 'orange', 'low': 'yellow'}

    for result in results:
        severity = severity_map[result[3]]
        symptoms.append([result[0],
                         '{first} {last}'.format(first=result[1], last=result[2]),
                         forms.issues[result[3]][1],
                         result[4],
                         result[5],
                         dateutil.parser.parse(result[6]).strftime('%Y/%m/%d %H:%M:%S'),
                         '{first} {last}'.format(first=result[7], last=result[8]),
                         result[9],
                         severity,
                         severity_colors[severity]
                         ])
    return flask.render_template('panel.html', symptoms=symptoms)


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
