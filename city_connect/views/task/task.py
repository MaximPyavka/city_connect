from flask import request, abort

import city_connect.models.user
from city_connect.views.task.base_task import BaseTaskView


class Task(BaseTaskView):
    def get(self, task_id):
        task = self.get_task(task_id)
        if not task:
            abort(400)
        return task

    def post(self, user_id):
        user = self.get_model(user_id, city_connect.models.user.User)
        if not user:
            abort(400)
        post_data = request.get_data()
        post_data["user_id"] = user.id
        task = self.create_task(**post_data)
        print(task)
        return task