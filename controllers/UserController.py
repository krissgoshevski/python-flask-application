from models.UserInfo import UserInfo, UserSpending, db
from flask import jsonify, request, Response
from sqlalchemy import func
import requests
import logging
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()


class UserController:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id


    @staticmethod
    def get_total_spending(user_id):
        try:
            # get the total spending for the user_id
            total_spending = db.session.query(func.sum(UserSpending.money_spent)).filter_by(user_id=user_id).scalar()

            user = UserInfo.query.get(user_id)

            if user is None:
                return jsonify({
                    'error': 'User not found'
                }), 404

            if total_spending is not None:
                response_data = {
                    'user_id': user_id,
                    'total_spending': float(total_spending)
                }
                return jsonify(response_data), 200
            else:
                return jsonify({'error': 'The user have not spent money alredy'}), 406
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()

    @staticmethod
    def get_average_spending_by_age():
        try:
            # Age ranges
            age_ranges = [(18, 24), (25, 30), (31, 36), (37, 47), (48, 99)]

            # Dictionary to store average spending for each age range
            average_spending_by_age = {}

            for min_age, max_age in age_ranges:
                # Query for average spending directly from the database
                query = db.session.query(
                    func.round(func.avg(UserSpending.money_spent), 1)
                ).join(UserInfo).filter(
                    UserInfo.age >= min_age,
                    UserInfo.age <= max_age
                )

                # Get the result of the query
                average_spending = query.scalar() or 0.0

                # Store the result in the dictionary
                average_spending_by_age[f'{min_age}-{max_age}'] = average_spending

            return jsonify(average_spending_by_age), 200

        except Exception as e:
            logging.error(f"Error in get_average_spending_by_age: {str(e)}")
            return jsonify({'error': 'Internal Server Error'}), 500

        finally:
            db.session.close()

    # FLASK API CLIENT SCRIPT
    @staticmethod
    def get_total_spending_by_users():
        try:
            # query for total spending for all users
            total_spending = db.session.query(db.func.sum(UserSpending.money_spent)).scalar()

            return jsonify({"total_spending_users": total_spending})
        except Exception as e:
            return jsonify({"error": str(e)}), 500





    @staticmethod
    def get_eligible_users():
        try:
            # the voucher could get if have spent more than 1000
            eligibility_threshold = 1000

            # Query users whose spending exceeds the eligibility threshold
            eligible_users = db.session.query(UserInfo). \
                join(UserSpending). \
                group_by(UserInfo.id). \
                having(func.sum(UserSpending.money_spent) > eligibility_threshold). \
                all()

            # Convert UserInfo to a JSON-serializable format
            eligible_users_data = []
            for user in eligible_users:
                user_data = {
                    'user_id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'age': user.age,
                }
                eligible_users_data.append(user_data)

            return jsonify({
                'users_for_voucher': eligible_users_data
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            db.session.close()


    @staticmethod
    def get_users_with_total_spending_above_1000():
        try:
            eligible_users = UserSpending.query.filter(UserSpending.money_spent > 999).all()

            eligible_users_data = []
            for user in eligible_users:
                user_data = {
                'user_id': user.user_id,
                'total_spending': user.money_spent
            }
                eligible_users_data.append(user_data)

            return jsonify(eligible_users_data), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    def store():
        try:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            age = data.get('age')
            password = data.get('password')

            if not name or not email or not age or not password:
                return jsonify({'error': 'Name, email, age and password are required'}), 400

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            new_user = UserInfo(name=name, email=email, age=age, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            return jsonify({
                'message': 'Successfully created user',
                'user': {
                    'id': new_user.id,
                    'name': new_user.name,
                    'email': new_user.email,
                    'age': new_user.age
                }
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def update(user_id):
        try:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            age = data.get('age')
            password = data.get('password')


            user = UserInfo.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404


            if name:
                user.name = name
            if email:
                user.email = email
            if age:
                user.age = age
            if password:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                user.password = hashed_password


            db.session.commit()

            return jsonify({
                'message': 'Successfully updated user',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'age': user.age
                }
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500



    @staticmethod
    def destroy(user_id):
        try:
            user = UserInfo.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            db.session.delete(user)
            db.session.commit()

            return jsonify({'message': 'User deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    def show(user_id):
        try:
            user = UserInfo.query.get(user_id)

            if user is None:
                return jsonify({'error': 'User not found'}), 404

            user_details = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'age': user.age,
                'created_at': str(user.created_at),
                'updated_at': str(user.updated_at)
            }

            return jsonify(user_details), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
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

    def send_statistics_to_telegram(self, statistics):
        bot_token = self.bot_token
        chat_id = self.chat_id
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

    def get_avg_spending_age_bot(self):
        avg_spending_age_url = 'http://127.0.0.1:5000/api/average_spending_by_age'
        response = requests.get(avg_spending_age_url)

        if response.status_code == 200:
            statistics = response.json()
            formatted_statistics = "\n".join(
                [f"{age_range}: {avg_spending}" for age_range, avg_spending in statistics.items()])
            result = self.send_statistics_to_telegram(formatted_statistics)
            return Response(result, status=200)
        else:
            return Response('Failed to retrieve statistics from API', status=response.status_code)


