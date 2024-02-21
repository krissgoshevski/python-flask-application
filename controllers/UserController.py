from models.UserInfo import UserInfo, UserSpending, db
from flask import jsonify, request
from sqlalchemy import func
import logging
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


class UserController:

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
            # age ranges
            age_ranges = [(18, 24), (25, 30), (31, 36), (37, 47), (48, 99)]

            #  dictionary to store average spending for each age range
            average_spending_by_age = {}

            for age_range in age_ranges:
                min_age, max_age = age_range

                #  total spending for users within the age range
                total_spending = db.session.query(func.sum(UserSpending.money_spent)). \
                    join(UserInfo).filter(UserInfo.age >= min_age, UserInfo.age <= max_age).scalar()

                # count of users within the age range
                user_count = db.session.query(func.count(UserInfo.id)).filter(UserInfo.age >= min_age,
                                                                              UserInfo.age <= max_age).scalar()

                # average spending if there are users in the age range
                if total_spending is not None and user_count > 0:
                    average_spending = float(total_spending) / user_count
                    average_spending_by_age[f'{min_age}-{max_age}'] = round(average_spending, 1)
                elif user_count > 0:
                    # case where total_spending is None
                    logging.warning(f"Total spending is None for age range {min_age}-{max_age}")
                    average_spending_by_age[f'{min_age}-{max_age}'] = 0.0
                else:
                    # case where there are no users in the age range
                    logging.warning(f"No users found for age range {min_age}-{max_age}")
                    average_spending_by_age[f'{min_age}-{max_age}'] = 0.0


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







