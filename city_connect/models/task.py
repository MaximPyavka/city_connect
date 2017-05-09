import datetime

from city_connect.app import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, user_id, description=''):
        self.title = title
        self.created = datetime.datetime.now()
        self.description = description
        self.user_id= user_id

    def __str__(self):
        return "ID: {}, TITLE: {}, CREATED: {}, BY: {}".format(self.id,
                                                               self.title,
                                                               self.created,
                                                               self.user_id)

    def __repr__(self):
        return "ID: {}, TITLE: {}, CREATED: {}, BY: {}".format(self.id,
                                                               self.title,
                                                               self.created,
                                                               self.user_id)
