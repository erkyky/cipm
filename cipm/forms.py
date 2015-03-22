import flask.ext.wtf as flask_wtf
import wtforms
import wtforms.validators as validators


class CipmForm(flask_wtf.Form):
    feedback = wtforms.TextAreaField('feedback', validators=[validators.DataRequired()])


class PatientForm(flask_wtf.Form):
    primary_issue_choices = [('0', 'Chest Pain'),
                             ('1', 'Shortness of Breath'),
                             ('2', 'Gained 2 Pounds Overnight'),
                             ('3', 'Out of Medication'),
                             ('4', 'High Blood Sugar'),
                             ('5', 'Other')]
    yes_no_emergency_choices = [('yes', 'yes'),
                                ('no', 'no')]
    weight_change_choices = [(str(x), str(x)) for x in xrange(2, 10, 1)]
    weight_change_choices += [('10', '10+')]

    primary_issue = wtforms.RadioField(label='primary_issue', choices=primary_issue_choices,
                                       validators=[validators.DataRequired()])
    chest_emergency = wtforms.RadioField(label='chest_emergency', choices=yes_no_emergency_choices,
                                         validators=[validators.Optional()])
    breath_emergency = wtforms.RadioField(label='breath_emergency', choices=yes_no_emergency_choices,
                                          validators=[validators.Optional()])
    weight_emergency = wtforms.SelectField(label='weight_emergency', choices=weight_change_choices,
                                           validators=[validators.Optional()])
    medication_emergency = wtforms.TextAreaField(label='medication_emergency', validators=[validators.Optional()])
    bloodsugar_emergency = wtforms.DecimalField(label='bloodsugar_emergency', validators=[validators.Optional()])
    other_emergency = wtforms.TextAreaField(label='other_emergency', validators=[validators.Optional()])




