import flask
import cipm
import cipm.forms as forms

@cipm.app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.CipmForm()
    if form.validate_on_submit():
        return flask.redirect('/thankyou')
    return flask.render_template('index.html', form=form)


@cipm.app.route('/patientform', methods=['GET', 'POST'])
def patient_form():
    form = forms.PatientForm()
    if form.validate_on_submit():
        return flask.redirect('/thankyou')
    return flask.render_template('patientform.html', form=form)


@cipm.app.route('/thankyou')
def thankyou():
    return flask.render_template('thanksyou.html')