import flask.ext.wtf as wtf
import wtforms
import wtforms.validators as validators
import cipm


issues = {'0': ('chest', 'Chest Pain'),
          '1': ('breath', 'Shortness of Breath'),
          '2': ('weight', 'Gained 2+ lbs Overnight'),
          '3': ('medication', 'Out of Medication'),
          '4': ('bloodsugar', 'High Blood Sugar'),
          '5': ('other', 'Other')}


class CipmForm(wtf.Form):
    feedback = wtforms.TextAreaField('feedback', validators=[validators.DataRequired()])


class PatientForm(wtf.Form):
    primary_issue_choices = [(k, v[1]) for k, v in sorted(issues.iteritems())]
    yes_no_emergency_choices = [('yes', 'Yes'),
                                ('no', 'No')]
    weight_change_choices = [(str(x), str(x)) for x in xrange(2, 10, 1)]
    weight_change_choices += [('10', '10+')]

    primary_issue = wtforms.RadioField(label='primary_issue', choices=primary_issue_choices,
                                       validators=[validators.DataRequired('Please select an option')])
    chest_emergency = wtforms.RadioField(label='chest_emergency', choices=yes_no_emergency_choices,
                                         validators=[validators.Optional()])
    breath_emergency = wtforms.RadioField(label='breath_emergency', choices=yes_no_emergency_choices,
                                          validators=[validators.Optional()])
    weight_emergency = wtforms.SelectField(label='weight_emergency', choices=weight_change_choices,
                                           validators=[validators.Optional()])
    medication_emergency = wtforms.TextAreaField(label='medication_emergency', validators=[validators.Optional()])
    bloodsugar_emergency = wtforms.DecimalField(label='bloodsugar_emergency', validators=[validators.Optional()])
    other_emergency = wtforms.TextAreaField(label='other_emergency', validators=[validators.Optional()])


class LoginForm(wtf.Form):
    email = wtforms.StringField('Email', validators=[validators.DataRequired(), validators.Length(1, 64),
                                                     validators.Email()])
    password = wtforms.PasswordField('Password', validators=[validators.DataRequired()])
    remember_me = wtforms.BooleanField('Keep me logged in')
    submit = wtforms.SubmitField('Log In')


class RegistrationForm(wtf.Form):
    email = wtforms.StringField('Email', validators=[validators.DataRequired(), validators.Length(1, 64),
                                           validators.Email()])
    username = wtforms.StringField('Username', validators=[
        validators.DataRequired(), validators.Length(1, 64), validators.Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = wtforms.PasswordField('Password', validators=[
        validators.DataRequired(), validators.EqualTo('password2', message='Passwords must match.')])
    password2 = wtforms.PasswordField('Confirm password', validators=[validators.DataRequired()])
    submit = wtforms.SubmitField('Register')

    def validate_email(self, field):
        db = cipm.get_db()
        cur = db.execute('''SELECT count(*) from users where email = ?''', [field.data])
        num_users = cur.fetchone()[0]
        if num_users > 0:
            raise validators.ValidationError('Email already registered. %s' % num_users)

    def validate_username(self, field):
        db = cipm.get_db()
        cur = db.execute('''SELECT count(*) from users where username = ?''', [field.data])
        num_users = cur.fetchone()[0]
        if num_users > 0:
            raise validators.ValidationError('Username already in use. %s' % num_users)