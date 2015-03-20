import flask.ext.wtf as flask_wtf
import wtforms
import wtforms.validators as validators


class CipmForm(flask_wtf.Form):
    feedback = wtforms.TextAreaField('feedback', validators=[validators.DataRequired()])
