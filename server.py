# -*- coding: utf-8 -*-

import json
import logging

import colander
from flask import (
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for
)
from flask.ext.session import Session

from jsonresume.schema.resume import Resume as ResumeSchema


app = Flask(__name__)
app.secret_key = 'RQtlBBBfHh9QbMSC99Ds'  # bad example, we should perhaps put it in an env var
app.config['SESSION_TYPE'] = 'filesystem'
app.debug = True
sess = Session()
sess.init_app(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'json'


@app.route('/', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        fil = request.files['file']
        if fil and allowed_file(fil.filename):
            try:
                data = json.load(fil)
                ResumeSchema().deserialize(data)
                flash("Success", category="success")
            except colander.Invalid as e:
                logging.exception("Invalid JSON resume content")
                flash(e, category="error")
        else:
            # no file detected
            flash('Please submit a JSON resume in the form', category="warning")

        return redirect(url_for('submit_form'))

if __name__ == '__main__':
    app.run()

