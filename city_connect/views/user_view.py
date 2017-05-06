from flask import render_template, flash, redirect, request
from base_view import BaseMethodView
from flask_login import login_user, logout_user, current_user, login_required
from city_connect.forms.forms import LoginForm, RegisterForm
from city_connect.models.user import User
from city_connect.config import LOGGING
import logging
import logging.config

logging.config.dictConfig(LOGGING) # ????

class RegistrationView(BaseMethodView):

    @staticmethod
    def get():
        form = RegisterForm()
        logging.debug('GET. Registration form rendered.')
        return render_template('main/registration.html', form=form)



    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            logging.debug('Registration template validated.')
            user = self.form_to_user(form)
            self.create_model(Model, **user)
            logging.debug('User {} created.'.format(user['login']))

            flash('You can now login.')
            flash('A confirmation email has been sent to you by email.')

            send_async_email(form.email.data,
                             'Your Account in Bookcrossing',
                             'email/greeting',
                             first_name=form.first_name.data)
            logging.debug('Email to {} sended.'.format(user['email']))
            logging.debug('User {} registered and can login.'
                          .format(user['login']))

            return redirect('/login/')

        logging.debug('User entered invalid values on submit. '
                      'Registration template rendered again.')
        return render_template('registration.html', form=form)

class UserSignIn(BaseMethodView):

    @staticmethod
    def get():
        form = LoginForm()
        logging.debug('Registration form rendered.')
        return render_template('user/signin.html')

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            logging.debug('Login form validated.')
            flag, user = self.verify_user(form)
            if flag:
                logging.debug('User {} is in DB.'.format(user.login))
                login_user(user)
                logging.debug('User {} is logged in and redirected.'
                              .format(user.login))
                return redirect(request.args.get('next') or '/profile/')

            flash('Invalid username or password.')
            logging.debug('User entered invalid values on submit. '
                          'Login form rendered again.')
        return render_template('user/signin.html')


class UserSignUp(BaseMethodView):

    @staticmethod
    @login_required
    def get():
        logout_user()
        logging.debug('User is logged out.')
        flash('You have been logged out!')
        logging.debug('Redirection to /login.')

        return render_template('user/signup.html')


