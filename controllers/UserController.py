from models.UserInfo import UserInfo, UserSpending, db
from flask import jsonify, request
from sqlalchemy import func
import logging



class UserController:

    @staticmethod
    def get_total_spending(user_id):
        try:
            # get the total spending for the user_id
            total_spending = db.session.query(func.sum(UserSpending.money_spent)).filter_by(user_id=user_id).scalar()

            if total_spending is not None:
                response_data = {
                    'user_id': user_id,
                    'total_spending': float(total_spending)
                }
                return jsonify(response_data), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()

    @staticmethod
    def get_average_spending_by_age():
        try:
            # Define age ranges
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