from flask import redirect, render_template,url_for,abort,flash
from blog import app


@app.route('/')
def index():
    return render_template('index.html')
