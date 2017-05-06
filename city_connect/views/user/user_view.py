from flask import render_template, request
from city_connect.views.user.user_base import BaseUsersView



class UserSignIn(BaseUsersView):
    def get(self):
        return render_template('user/signin.html')


class UserSignUp(BaseUsersView):
    def get(self):
        return render_template('user/signup.html')
    def post(self):
        print(request.form)
        return render_template('user/signup.html')
