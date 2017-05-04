from city_connect.resources.base_resource import BaseResource

class HelloWorld(BaseResource):
    def get(self):
        return {'hello': 'GET',
                "success": True}

    def post(self):
        return {'hello': 'POST',
                "success": True}
