import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '../..'))

from flask_testing import TestCase

from city_connect.app import db, app
from city_connect.config import TestingConfig


class BaseTestCase(TestCase):
    def create_app(self, app=app):
        app.config.from_object(TestingConfig)
        return app

    def setUp(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
