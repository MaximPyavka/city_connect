import datetime

from city_connect.app import db
from city_connect.models.user import User


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, User.id())

    def __init__(self, title, created_by, description=''):
        self.title = title
        self.created = datetime.datetime.now()
        self.description = description
        self.created_by = created_by

    def __str__(self):
        return "ID: {}, TITLE: {}, CREATED: {}, BY: {}".format(self.id,
                                                               self.title,
                                                               self.created,
                                                               self.created_by)

    def __repr__(self):
        return "ID: {}, TITLE: {}, CREATED: {}, BY: {}".format(self.id,
                                                               self.title,
                                                               self.created,
                                                               self.created_by)
