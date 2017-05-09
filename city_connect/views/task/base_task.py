import city_connect.models.task

from city_connect.views.base_view import BaseMethodView


class BaseTaskView(BaseMethodView):
    def create_task(self, **kwargs):
        return self.create_model(city_connect.models.task.Task, **kwargs)

    def get_task(self, task_id):
        return self.get_model(task_id, city_connect.models.task.Task)
