from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from blog.settings import config

app = Flask('blog')
config_name = os.getenv('FLASK_CONFIG', 'development')
app.config.from_object(config[config_name])
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)

from blog import views, errors, commands


