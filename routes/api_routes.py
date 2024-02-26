from flask import Blueprint
from controllers.UserController import UserController
import os
from dotenv import load_dotenv

# Loading environment variables from .env
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
api_routes = Blueprint('api_routes', __name__)
user_controller = UserController(BOT_TOKEN, CHAT_ID)

@api_routes.route('/users', methods=['GET'])
def get_all_users():
    return UserController.get_all_users()

@api_routes.route('/user/show/<user_id>', methods=['GET'])
def show(user_id):
    return UserController.show(user_id)

@api_routes.route('/user/create', methods=['POST'])
def store():
    return UserController.store()

@api_routes.route('/user/edit/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return UserController.update(user_id)

@api_routes.route('/user/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return UserController.destroy(user_id)


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


@api_routes.route('/bot', methods=['GET'])
def get_avg_spending_age_bot():
    return user_controller.get_avg_spending_age_bot()
