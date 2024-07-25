from functools import wraps
import jwt
from flask import request, make_response
from database.models import Users


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers['Authorization']
        if not token:
            return make_response(
                {
                    'message': 'Token is missing',
                }, 401
            )

        try:
            data = jwt.decode(token, 'secret', algorithms=['HS256'])
            current_user = Users.query.filter_by(id=data.get('id')).first()
            print(current_user)
        except Exception as e:
            return make_response(
                {
                    'message': 'Token is invalid',
                }, 401
            )
        return f(current_user, *args, **kwargs)
    return decorated
