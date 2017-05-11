import os

from flask import request, abort, render_template, send_from_directory, url_for, redirect
from werkzeug.utils import secure_filename

import city_connect.models.user
from city_connect.views.task.base_task import BaseTaskView
from city_connect.app import app


class Task(BaseTaskView):
    def get(self, task_id=None):
        if not task_id:
            return render_template('task/create-task.html')
        task = self.get_task(task_id)
        if not task:
            return render_template('task/create-task.html')
            # abort(400)
        return render_template('task/create-task.html')

    def post(self):
        post_data = {
            "title": request.form.get('title'),
            "description": request.form.get('description'),
            "user_id": request.form.get('user_id')
        }
        user = self.get_model(post_data.get('user_id'), city_connect.models.user.User)
        if not user:
            abort(400)

        # check if the post request has the file part
        if request.files:
            file = request.files['photo']
            if file.filename == '':
                return redirect(request.url)
            if file and self.allowed_file(file.filename):
                filename = self.generate_filename(secure_filename(file.filename))
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                post_data['image_url'] = file_path
                file.save(file_path)
        self.create_task(**post_data)
        return redirect(url_for('index'), 200)


class DisplayTasks(BaseTaskView):
    def get(self):
        return render_template('task/task-details.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
