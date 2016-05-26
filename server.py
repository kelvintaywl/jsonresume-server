# -*- coding: utf-8 -*-

import json
import logging

import colander
from flask import (
    Flask,
    jsonify,
    make_response,
    render_template,
    request
)

from jsonresume.schema.resume import Resume as ResumeSchema


app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'json'


@app.route('/', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        fil = request.files['file']
        if fil and allowed_file(fil.filename):
            print('data')
            try:
                data = json.load(fil)
                print("data: {}".format(data))
                ResumeSchema().deserialize(data)
            except colander.Invalid as e:
                logging.exception("Invalid JSON resume content")
                err_resp = make_response(json.dumps(e), 400)
                err_resp.headers['Content-Type'] = 'application/json'
                return err_resp

            return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run()

