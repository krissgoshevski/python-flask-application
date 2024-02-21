from flask import Blueprint, jsonify, Response, request, url_for
from controllers.UserController import UserController
import requests
from models.UserInfo import UserInfo


api_routes = Blueprint('api_routes', __name__)


@api_routes.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = UserInfo.query.all()
        user_data = []
        for user in users:
            user_data.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'age': user.age,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None,
            })
        return jsonify({'users': user_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
        formatted_statistics = "\n".join(
             [f"{age_range}: {avg_spending}" for age_range, avg_spending in statistics.items()])
        result = send_statistics_to_telegram(formatted_statistics)
        return Response(result, status=200)
    else:
        return Response('Failed to retrieve statistics from API', status=response.status_code)

