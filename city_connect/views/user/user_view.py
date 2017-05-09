from flask import request
from flask import render_template
from city_connect.views.user.user_base import BaseUsersView
from flask_login import current_user, login_required


class UserSignIn(BaseUsersView):
    def get(self):
        return render_template('user/signin.html')


class UserSignUp(BaseUsersView):
    def get(self):
        return render_template('user/signup.html')

    def post(self):
        for k in request.form:
            print("================================")
            print(request.form.get(k))
        return render_template('user/signup.html')


class LoginUserCheck(BaseUsersView):
    @login_required
    def get(self):
        return "OK", 200
