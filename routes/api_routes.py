from flask import Blueprint, jsonify, Response, request, url_for
from controllers.UserController import UserController
import requests


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





#########################################################
#########################################################

def send_statistics_to_telegram(statistics):
    bot_token = '6747198782:AAET-fEvkHlp2PUpYzDK_4HG-RFOsRBvgDw'
    chat_id = 6273167095
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': statistics
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return 'Statistics sent successfully!'
    else:
        return 'Failed to send statistics to Telegram.'


@api_routes.route('/test/bot', methods=['GET'])
def get_avg_spending_age_bot():
    avg_spending_age_url = 'http://127.0.0.1:5000/api/average_spending_by_age'
    response = requests.get(avg_spending_age_url)

    if response.status_code == 200:
        statistics = response.json()
        # formatted_statistics = "\n".join(
        #     [f"{age_range}: {avg_spending}" for age_range, avg_spending in statistics.items()])
        result = send_statistics_to_telegram(statistics)
        return Response(result, status=200)
    else:
        return Response('Failed to retrieve statistics from API', status=response.status_code)

