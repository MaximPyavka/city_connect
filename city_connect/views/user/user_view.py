from flask import render_template
from city_connect.views.base_view import BaseMethodView



class UserSignIn(BaseMethodView):
    def get(self):
        return render_template('user/signin.html')


class UserSignUp(BaseMethodView):
    def get(self):
        return render_template('user/signup.html')
