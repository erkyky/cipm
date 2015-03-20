import flask
import cipm
import cipm.forms as forms

@cipm.app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.CipmForm()
    if form.validate_on_submit():
        pass
    return flask.render_template('index.html', form=form)