import logging
from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from logging.handlers import StreamHandler

app = Flask(__name__)
app.config.from_object(Config)
# TODO: Add any logging levels and handlers with app.logger
Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

stream_handler = StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)

@app.before_first_request
def setup_logging():
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_logger.handlers)
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.addHandler(stream_handler)

    gunicorn_logger.info('Application initialized')

    @app.after_request
    def after_request(response):
        app.logger.info('{} {} {}'.format(request.method, request.path, response.status_code))
        return response

import FlaskWebProject.views
