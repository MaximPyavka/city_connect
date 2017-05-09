import string
import random

import city_connect.models.task
from city_connect.config import BaseConfig

from city_connect.views.base_view import BaseMethodView


class BaseTaskView(BaseMethodView):
    def create_task(self, **kwargs):
        return self.create_model(city_connect.models.task.Task, **kwargs)

    def get_task(self, task_id):
        return self.get_model(task_id, city_connect.models.task.Task)

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in BaseConfig.ALLOWED_EXTENSIONS

    def generate_filename(self, filename):
        return ''.join([random.choice(string.ascii_letters) for i in range(32)]) + filename[-4:]
