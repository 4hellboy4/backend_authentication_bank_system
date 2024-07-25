from sqlalchemy import func
from flask import request, make_response, Blueprint
from database.models import Users, Funds
from database.database import db
from endpoints.decorators import token_required

funds = Blueprint(name='funds', import_name="funds_router", url_prefix='/funds')


@funds.route('/get', methods=['GET'])
@token_required
def get_all_funds(current_user, *args, **kwargs):
    funds = Funds.query.filter_by(userId=current_user.id).all()
    total_sum = 0
    if funds:
        total_sum = db.session.query(db.func.round(func.sum(Funds.amount), 2)).filter_by(userId=current_user.id).scalar() or 0
    return make_response(
        {
            'data': [row.serialize for row in funds],
            'sum': total_sum,
        }, 200
    )


@funds.route('/add', methods=['POST'])
@token_required
def add_fund(current_user, *args, **kwargs):
    data = request.json
    if data.get('amount'):
        fund = Funds(amount=data.get('amount'), userId=current_user.id)
        db.session.add(fund)
        db.session.commit()
        return make_response(
            {
                'message': 'Fund added successfully',
                'data': fund.serialize,
            }, 201
        )
    else:
        return make_response(
            {
                'message': 'Amount not provided',
            }, 400
        )


@funds.route("/get/<int:id>", methods=['GET'])
@token_required
def get_fund(current_user, id, *args, **kwargs):
    try:
        fund = Funds.query.filter_by(id=id).first()
        if not fund:
            return make_response(
                {
                    'message': "Unable to get fund",
                }
            )
        return make_response(
            {
                'data': fund.serialize,
            }
        )
    except Exception as e:
        print(e)
        return make_response(
            {
                "message": str(e),
            }
        )

@funds.route('/update/<int:id>', methods=['PUT'])
@token_required
def update_fund(current_user, id, *args, **kwargs):
    try:
        fund = Funds.query.filter_by(userId=current_user.id, id=id).first()
        if not fund:
            return make_response(
                {
                    'message': 'Fund not found',
                }, 409
            )
        data = request.json
        amount = data.get('amount')
        if amount:
            fund.amount = amount
        db.session.commit()
        return make_response({
            'message': 'Fund updated successfully',
            'data': fund.serialize,
        }, 200)
    except Exception as e:
        print(e)
        return make_response(
            {
                'message': f'Unable to update: {e}',
            }, 409
        )

@funds.route('/delete/<int:id>', methods=['DELETE'])
@token_required
def delete_fund(current_user, id, *args, **kwargs):
    try:
        fund = Funds.query.filter_by(userId=current_user.id, id=id).first()
        if not fund:
            return make_response(
                {
                    'message': f'Fund with {id} not found',
                }, 409
            )
        db.session.delete(fund)
        db.session.commit()
        return make_response({
            'message': "Fund deleted successfully",
        }, 200)
    except Exception as e:
        print(e)
        return make_response(
            {
                'message': 'Unable to delete fund',
            }, 409
        )
