from flask_restful import Resource
from flask_sqlalchemy import Model
from sqlalchemy.exc import ProgrammingError, IntegrityError
from sqlalchemy.orm.exc import ObjectDeletedError, StaleDataError, NoResultFound, MultipleResultsFound
from marshmallow_sqlalchemy import ModelSchema

from city_connect.app import db


class BaseResource(Resource):
    def create_model(self, model: Model, *args, **kwargs) -> Model or None:
        m = model(*args, **kwargs)
        db.session.add(m)
        try:
            db.session.commit()
        except(ProgrammingError, IntegrityError):
            return None
        else:
            return m

    def delete_model(self, mid: int, model: Model) -> Model or None:
        m = self.get_model(mid, model)
        if not m:
            return None
        db.session.delete(m)
        try:
            db.session.commit()
        except(ObjectDeletedError, StaleDataError):
            return None
        else:
            return m

    def get_model(self, mid: int, model: Model) -> Model or None:
        try:
            m = model.query.get(mid)
        except(NoResultFound, MultipleResultsFound):
            return None
        else:
            return m

    def update_model(self, mid: int, model: Model, data: dict) -> Model or None:
            m = self.get_model(mid, model)
            if m and data:
                for k in data:
                    if hasattr(m, k):
                        setattr(m, k, data[k])
                    else:
                        return None

                db.session.add(m)
                try:
                    db.session.commit()
                except(ProgrammingError, IntegrityError):
                    return None
                else:
                    return m
            else:
                return None

    def serialize_model(self, mid: int, model: Model, schema: ModelSchema) -> Model or None:
        m = self.get_model(mid, model)
        if m:
            serialized_model = schema.dump(m).data
            return serialized_model
        else:
            return None
