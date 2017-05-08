import unittest
import json
import time

from city_connect.app import db
from city_connect.models.black_list_token import BlacklistToken
from city_connect.models.user import User
from city_connect.tests.tests_config import BaseTestCase


class TestUserModel(BaseTestCase):
    def test_create_user(self):
        user = self._create_user()
        self.assertNotEqual(User.query.get(user.id), None)

    def test_encode_auth_token(self):
        user = self._create_user()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = self._create_user()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(user.decode_auth_token(auth_token.decode("utf-8")) == 1)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        user = self._create_user()
        with self.client:
            data = json.dumps(self._create_user_dict())
            response = self.client.post(
                'api/v1/auth/register',
                data=data,
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertFalse(data['success'])
            self.assertEqual(data['message'], 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            resp_register = self.client.post(
                'api/v1/auth/register',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456',
                    login='joe'
                )),
                content_type='application/json',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertEqual(data_register['success'], True)
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = self.client.post(
                'api/v1/auth/login',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456',
                    login="joe"
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['success'], True)
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = self.client.post(
                'api/v1/auth/login',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='wrong_pass',
                    login="joe123"
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['success'], False)
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_user_status(self):
        """ Test for user status """
        with self.client:
            resp_register = self.client.post(
                'api/v1/auth/register',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456',
                    login='joe'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                'api/v1/auth/status',
                headers=dict(
                    Authorization=json.loads(resp_register.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['success'], True)
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == 'joe@gmail.com')
            self.assertTrue(data['data']['admin'] is 'true' or 'false')
            self.assertEqual(response.status_code, 200)

    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            # user registration
            resp_register = self.client.post(
                'api/v1/auth/register',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456',
                    login='joe'
                )),
                content_type='application/json',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertEqual(data_register['success'], True)
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.client.post(
                'api/v1/auth/login',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456',
                    login='joe'
                )),
                content_type='application/json'
            )
            data_login = json.loads(resp_login.data.decode())
            self.assertEqual(data_login['success'], True)
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # valid token logout
            response = self.client.post(
                'api/v1/auth/logout',
                headers=dict(
                    Authorization=json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['success'], True)
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout(self):
        """ Testing logout after the token expires """
        with self.client:
            # user registration
            resp_register = self.client.post(
                'api/v1/auth/register',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456',
                    login='joe'
                )),
                content_type='application/json',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertEqual(data_register['success'], True)
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.client.post(
                'api/v1/auth/login',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456',
                    login='joe'
                )),
                content_type='application/json'
            )
            data_login = json.loads(resp_login.data.decode())
            self.assertEqual(data_login['success'], True)
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # invalid token logout
            time.sleep(6)
            response = self.client.post(
                'api/v1/auth/logout',
                headers=dict(
                    Authorization=json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['success'], False)
            self.assertTrue(data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_logout(self):
        """ Test for logout after a valid token gets blacklisted """
        with self.client:
            # user registration
            resp_register = self.client.post(
                'api/v1/auth/register',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456',
                    login='joe'
                )),
                content_type='application/json',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertEqual(data_register['success'], True)
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # user login
            resp_login = self.client.post(
                'api/v1/auth/login',
                data=json.dumps(dict(
                    email='joe@gmail.com',
                    password='123456',
                    login='joe'
                )),
                content_type='application/json'
            )
            data_login = json.loads(resp_login.data.decode())
            self.assertEqual(data_login['success'], True)
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            self.assertTrue(resp_login.content_type == 'application/json')
            self.assertEqual(resp_login.status_code, 200)
            # blacklist a valid token
            blacklist_token = BlacklistToken(token=json.loads(resp_login.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            # blacklisted valid token logout
            response = self.client.post(
                'api/v1/auth/logout',
                headers=dict(
                    Authorization=json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['success'], False)
            self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def _create_user(self):
        user = User(
            email='test@test.com',
            password='test',
            login="test_user",
        )
        db.session.add(user)
        db.session.commit()
        return user

    def _create_user_dict(self):
        return {
            "email": 'test@test.com',
            "password": 'test',
            "login": "test_user",
        }


if __name__ == '__main__':
    unittest.main()
