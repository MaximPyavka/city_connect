import bcrypt
from flask import abort, request

import city_connect.models.user
from city_connect.app import db
from city_connect.models.black_list_token import BlacklistToken
from city_connect.resources.user.base_user import BaseResourceUser


class UserLogin(BaseResourceUser):
    """ User Login Resource """

    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = city_connect.models.user.User.query.filter_by(
                phone_number=post_data.get('phone'), phone_code=post_data.get('phone_code')
            ).first()
            if user:
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    responseObject = {
                        'success': True,
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    user.phone_code = ""
                    db.session.add(user)
                    db.session.commit()
                    return self.make_response(responseObject, status=200)
            else:
                responseObject = {
                    'success': False,
                    'message': 'User does not exist.'
                }
                return self.make_response(responseObject, status=404)
        except Exception as e:
            print(e)
            responseObject = {
                'success': False,
                'message': 'Try again'
            }
            return self.make_response(responseObject, status=500)


class UserRegister(BaseResourceUser):
    """ User Registration Resource """

    def post(self):
        # get the post data
        post_data = request.get_json()
        if not post_data:
            abort(400)
        # check if user already exists
        user = city_connect.models.user.User.query.filter_by(phone_number=post_data.get('phone')).first()
        if not user:
            try:
                data = dict(phone_number=post_data.get('phone'),
                            phone_code=self.generate_phone_code()
                            )
                user = self.create_user(**data)
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'success': True,
                    'message': 'Successfully registered.',
                    'phone_code': user.phone_code
                }
                return self.make_response(responseObject, status=201)
            except Exception as e:
                print(e)
                responseObject = {
                    'success': False,
                    'message': 'Some error occurred. Please try again.'
                }
                return self.make_response(responseObject, status=401)
        else:
            phone_code = self.generate_phone_code()
            responseObject = {
                'success': True,
                'message': 'User already exists. Please Log in.',
                'phone_code': phone_code
            }
            user.phone_code = phone_code
            db.session.add(user)
            db.session.commit()
            return self.make_response(responseObject, status=202)


class UserLogout(BaseResourceUser):
    """ Logout Resource """

    def post(self):
        # get auth token
        auth_token = request.headers.get('Authorization')
        if auth_token:
            resp = self.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    responseObject = {
                        'success': True,
                        'message': 'Successfully logged out.'
                    }
                    return self.make_response(responseObject, status=200)
                except Exception as e:
                    responseObject = {
                        'success': False,
                        'message': e
                    }
                    return self.make_response(responseObject, status=200)
            else:
                responseObject = {
                    'success': False,
                    'message': resp
                }
                return self.make_response(responseObject, status=401)
        else:
            responseObject = {
                'success': False,
                'message': 'Provide a valid auth token.'
            }
            return self.make_response(responseObject, status=403)

class UserStatus(BaseResourceUser):
    def get(self):
        # get the auth token
        auth_token = request.headers.get('Authorization')
        if auth_token:
            resp = self.decode_auth_token(auth_token)

            if not isinstance(resp, str):
                user = city_connect.models.user.User.query.filter_by(id=resp).first()
                responseObject = {
                    'success': True,
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': user.registered_on.isoformat()
                    }
                }
                return self.make_response(responseObject, status=200)
            responseObject = {
                'success': False,
                'message': resp
            }
            return self.make_response(responseObject, status=401)
        else:
            responseObject = {
                'success': False,
                'message': 'Provide a valid auth token.'
            }
            return self.make_response(responseObject, status=401)
