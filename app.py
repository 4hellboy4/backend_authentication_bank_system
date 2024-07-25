from flask import Flask
from database.database import db

from endpoints.funds import funds as funds_router
from endpoints.authentication import auth as auth_router
from endpoints.base import router as base_router

# app = Flask(__name__, template_folder='templates')
#
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user:password@localhost:5432/postgres"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
#
# db.init_app(app)

# api = Blueprint('api', import_name='api', url_prefix='/')


# @app.post('/signup', methods=['POST'])
# def sign_up():
#     data: json = request.json
#     email = data.get('email')
#     password = data.get('password')
#     first_name = data.get('firstName')
#     last_name = data.get('lastName')
#
#     if first_name and last_name and email and password:
#         user = Users.query.filter_by(email=email).first()
#         if user:
#             return make_response(
#                 {
#                     'message': 'Please sign in'
#                 }, 200
#             )
#         user = Users(
#             email=email,
#             password=generate_password_hash(password),
#             firstName=first_name,
#             lastName=last_name,
#         )
#         db.session.add(user)
#         db.session.commit()
#         return make_response(
#             {
#                 'message': "User created successfully",
#             }, 201
#         )
#     return make_response(
#         {
#             'message': 'Unable to create User'
#         }, 500
#     )
#
#
# @app.post('/login', methods=['POST'])
# def login():
#     auth = request.json
#     if not auth or not auth.get('email') or not auth.get('password'):
#         return make_response(
#             {
#                 'message': 'Proper credentials were not provided',
#             }, 401
#         )
#
#     user = Users.query.filter_by(email=auth.get('email')).first()
#
#     if not user:
#         return make_response(
#             {
#                 'message': 'Please make an account',
#             }
#         )
#
#     if check_password_hash(user.password, auth.get('password')):
#         token = jwt.encode({
#             'id': user.id,
#             'exp': datetime.utcnow() + timedelta(minutes=30),
#         },
#             'secret',
#             "HS256"
#         )
#
#         return make_response({
#             'token': token
#         }, 201
#         )
#
#     return make_response(
#         {
#             'message': 'Invalid credentials',
#         }, 401
#     )


# def token_required(f):
#
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if "Authorization" in request.headers:
#             token = request.headers['Authorization']
#         if not token:
#             return make_response(
#                 {
#                     'message': 'Token is missing',
#                 }, 401
#             )
#
#         try:
#             data = jwt.decode(token, 'secret', algorithms=['HS256'])
#             current_user = Users.query.filter_by(id=data.get('id')).first()
#             print(current_user)
#         except Exception as e:
#             return make_response(
#                 {
#                     'message': 'Token is invalid',
#                 }, 401
#             )
#         return f(current_user, *args, **kwargs)
#     return decorated


# @app.route('/funds', methods=['GET'])
# @token_required
# def get_all_funds(current_user, *args, **kwargs):
#     funds = Funds.query.filter_by(userId=current_user.id).all()
#     total_sum = 0
#     if funds:
#         total_sum = Funds.query.with_entities(db.func.round(func.sum(Funds.amount), 2)).filter_by(userId=current_user.id).all()[0][0]
#     return make_response(
#         {
#             'data': [row.serialize for row in funds],
#             'sum': total_sum,
#         }, 200
#     )
#
#
# @app.route('/funds', methods=['POST'])
# @token_required
# def add_fund(current_user, *args, **kwargs):
#     data = request.json
#     if data.get('amount'):
#         fund = Funds(amount=data.get('amount'), userId=current_user.id)
#         db.session.add(fund)
#         db.session.commit()
#     return fund.serialize
#
# @app.route("/funds/<id>", methods=['GET'])
# @token_required
# def get_fund(current_user, id, *args, **kwargs):
#     try:
#         fund = Funds.query.filter_by(id=id).first()
#         if not fund:
#             return make_response(
#                 {
#                     'message': "Unable to get fund",
#                 }
#             )
#         return make_response(
#             {
#                 'data': fund.serialize,
#             }
#         )
#     except Exception as e:
#         print(e)
#         return make_response(
#             {
#                 "message": str(e),
#             }
#         )
#
#
# @app.route('/funds/<id>', methods=['PUT'])
# @token_required
# def update_fund(current_user, id, *args, **kwargs):
#     try:
#         funds = Funds.query.filter_by(userId=current_user.id, id=id).first()
#         if not funds:
#             return make_response(
#                 {
#                     'message': 'Fund not found',
#                 }, 409
#             )
#         data = request.json
#         amount = data.get('amount')
#         if amount:
#             funds.amount = amount
#         db.session.commit()
#         return make_response({
#             'message': funds.serialize,
#         }, 200)
#     except Exception as e:
#         print(e)
#         return make_response(
#             {
#                 'message': f'Unable to update: {e}',
#             }, 409
#         )
#
#
# @app.route('/funds/<id>', methods=['DELETE'])
# @token_required
# def delete_fund(current_user, id, *args, **kwargs):
#     try:
#         fund = Funds.query.filter_by(userId=current_user.id, id=id).first()
#         if not fund:
#             return make_response(
#                 {
#                     'message': f'Fund with {id} not found',
#                 }, 409
#             )
#         db.session.delete(fund)
#         db.session.commit()
#         return make_response({
#             'message': "Deleted",
#         }, 200)
#     except Exception as e:
#         print(e)
#         return make_response(
#             {
#                 'message': 'Unable to update',
#             }, 409
#         )




if __name__ == '__main__':
    app = Flask(__name__, template_folder='templates/', static_folder='static', static_url_path='/')

    app.register_blueprint(auth_router)
    app.register_blueprint(funds_router)
    app.register_blueprint(base_router)

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user:password@localhost:5432/postgres"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=8000, debug=True)
