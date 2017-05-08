import json

from city_connect.resources.base_resource import BaseResource
from city_connect.app import app
import city_connect.models.user


class BaseResourceUser(BaseResource):
    def create_user(self, **kwargs):
        return self.create_model(city_connect.models.user.User, **kwargs)

    def make_response(self, responseObject, status):
        return app.response_class(
            response=json.dumps(responseObject),
            status=status,
            mimetype='application/json'
        )

    def decode_auth_token(self, token):
        return city_connect.models.user.User.decode_auth_token(
            city_connect.models.user.User,
            token
        )
