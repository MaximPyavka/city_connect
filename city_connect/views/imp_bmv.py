import sys,os

print(sys.path)
print(os.listdir())

from base_view import BaseMethodView

class BaseCheck(BaseMethodView):
    pass

a= BaseCheck.__class__
print(a)

from flask import render_template

class UserSignIn(BaseMethodView):
    def get(self):
        return render_template('user/signin.html')

from city_connect.models.user import User

user = User(
    email=form.email.data,
    password=form.password.data,
    confirmed=False
)