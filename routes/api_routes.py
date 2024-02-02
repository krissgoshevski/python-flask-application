from flask import Blueprint
from controllers.UserController import UserController

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/total_spent/<int:user_id>', methods=['GET'])
def get_total_spending(user_id):
    return UserController.get_total_spending(user_id)

@api_routes.route('/average_spending_by_age', methods=['GET'])
def get_average_spending_by_age():
    return UserController.get_average_spending_by_age()


# # get_average_spending_by_age_telegram_bot_api
# @api_routes.route('/average_spending_by_age_telegram_bot_api', methods=['GET'])
# def get_average_spending_by_age_bot():
#     return UserController.get_average_spending_by_age_telegram_bot_api()
#
