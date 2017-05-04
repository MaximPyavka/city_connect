import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from city_connect.config import runtime_config
from flask_assets import Environment, Bundle
from flask_restful import Api


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# dev, prod, test
APP_STATUS = 'dev'


app = Flask(__name__)
app.config.from_object(runtime_config(APP_STATUS))

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

api = Api(app, prefix='/api/v1')

assets = Environment(app)

# create and register assets
css = Bundle(
    'styles/*.css',
    filters='cssmin',
    output='styles/tmp/main.min.css'
)

js = Bundle(
    'scripts/*.js',
    'scripts/**/*.js',
    filters='jsmin',
    output='scripts/tmp/main.min.js'
)

assets.register('css_all', css)
assets.register('js_all', js)


# application routes
from city_connect.views.index import Index, TEST_500
from city_connect.views.user.user_view import (
    UserSignIn,
    UserSignUp
)

index_view = Index.as_view('index')
app.add_url_rule('/', view_func=index_view, methods=['GET'])

app.add_url_rule('/test-500', view_func=TEST_500.as_view("test-500"), methods=['GET'])

app.add_url_rule('/sign-in', view_func=UserSignIn.as_view("sign-in"), methods=['GET'])
app.add_url_rule('/sign-up', view_func=UserSignUp.as_view("sign-up"), methods=['GET'])

# api urls
from city_connect.resources.hello_world import HelloWorld
api.add_resource(HelloWorld, '/')


# error handlers
from city_connect.views.error_handlers import (
    page_not_found,
    forbidden,
    gone,
    internal_server_error,
)

app.register_error_handler(404, page_not_found)
app.register_error_handler(403, forbidden)
app.register_error_handler(410, gone)
app.register_error_handler(500, internal_server_error)
