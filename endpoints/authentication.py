from datetime import datetime, timedelta
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, make_response, Blueprint
import json
from database.models import Users
from database.database import db

auth = Blueprint(name='auth', url_prefix='/auth', import_name="auth_router")

@auth.route('/signup', methods=['POST'])
def sign_up():
    data: json = request.json
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')

    if first_name and last_name and email and password:
        user = Users.query.filter_by(email=email).first()
        if user:
            return make_response(
                {
                    'message': 'Please sign in'
                }, 200
            )
        user = Users(
            email=email,
            password=generate_password_hash(password),
            firstName=first_name,
            lastName=last_name,
        )
        db.session.add(user)
        db.session.commit()
        return make_response(
            {
                'message': "User created successfully",
            }, 201
        )
    return make_response(
        {
            'message': 'Unable to create User'
        }, 500
    )


@auth.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response(
            {
                'message': 'Proper credentials were not provided',
            }, 401
        )

    user = Users.query.filter_by(email=auth.get('email')).first()

    if not user:
        return make_response(
            {
                'message': 'Please make an account',
            }
        )

    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30),
        },
            'secret',
            "HS256"
        )

        return make_response({
            'token': token
        }, 201
        )

    return make_response(
        {
            'message': 'Invalid credentials',
        }, 401
    )
