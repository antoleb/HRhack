from flask import render_template

from .app import app


@app.route('/', methods=['GET'])
def test_page():
    return render_template('test.html')
