from flask import Blueprint, jsonify, Response
from controllers.UserController import UserController

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/total_spent/<int:user_id>', methods=['GET'])
def get_total_spending(user_id):
    return UserController.get_total_spending(user_id)

@api_routes.route('/average_spending_by_age', methods=['GET'])
def get_average_spending_by_age():
    return UserController.get_average_spending_by_age()






# for flask script api's
@api_routes.route('/total_spending_users', methods=['GET'])
def get_total_spending_by_users():
    return UserController.get_total_spending_by_users()


@api_routes.route('/users/vouchers', methods=['GET'])
def get_users_with_vouchers():
    return UserController.get_eligible_users()



@api_routes.route('/total_spending_above_1000', methods=['GET'])
def total_spending_above_thousand():
    return UserController.get_users_with_total_spending_above_1000()
