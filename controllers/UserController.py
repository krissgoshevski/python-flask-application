from models.UserInfo import UserInfo, UserSpending, db
from flask import jsonify
from sqlalchemy import func
import logging


from telegram import Bot



# TELEGRAM_BOT_TOKEN = '6747198782:AAET-fEvkHlp2PUpYzDK_4HG-RFOsRBvgDw'
# telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)



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


    # @staticmethod
    # async def get_average_spending_by_age_telegram_bot_api():
    #     try:
    #         age_ranges = [(18, 24), (25, 30), (31, 36), (37, 47), (48, 99)]
    #         average_spending_by_age = {}
    #
    #         for age_range in age_ranges:
    #             min_age, max_age = age_range
    #
    #             total_spending = db.session.query(func.sum(UserSpending.money_spent)). \
    #                 join(UserInfo).filter(UserInfo.age >= min_age, UserInfo.age <= max_age).scalar()
    #
    #             user_count = db.session.query(func.count(UserInfo.id)).filter(UserInfo.age >= min_age,
    #                                                                           UserInfo.age <= max_age).scalar()
    #
    #             if total_spending is not None and user_count > 0:
    #                 average_spending = float(total_spending) / user_count
    #                 average_spending_by_age[f'{min_age}-{max_age}'] = round(average_spending, 1)
    #             elif user_count > 0:
    #                 logging.warning(f"Total spending is None for age range {min_age}-{max_age}")
    #                 average_spending_by_age[f'{min_age}-{max_age}'] = 0.0
    #             else:
    #                 logging.warning(f"No users found for age range {min_age}-{max_age}")
    #                 average_spending_by_age[f'{min_age}-{max_age}'] = 0.0
    #
    #         # Convert the result to JSON
    #         statistics_json = jsonify(average_spending_by_age).get_data(as_text=True)
    #
    #         # Send the statistics to the Telegram channel
    #         telegram_channel_id = 'StoreStatsBot'  # Replace with your actual channel username
    #         await UserController.send_telegram_message(telegram_channel_id, f"Statistics: {statistics_json}")
    #
    #
    #
    #         return jsonify(average_spending_by_age), 200
    #
    #     except Exception as e:
    #         logging.error(f"Error in get_average_spending_by_age_telegram_bot_api: {str(e)}")
    #
    #         return jsonify({'error': 'Internal Server Error'}), 500
    #
    #     finally:
    #         db.session.close()

    # @staticmethod
    # async def send_telegram_message(channel_id, message):
    #     await telegram_bot.send_message(channel_id, message)





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

            return jsonify({
                'users_for_voucher': eligible_users
            })

        except Exception as e:
            raise

    @staticmethod
    def write_eligible_users_to_mongodb(eligible_users):
        try:

            for user in eligible_users:
                db.users_vouchers.vouchers.insert_one({
                    "user_id": user.id,
                    "total_spending": float(db.session.query(func.sum(UserSpending.money_spent)).
                                            filter_by(user_id=user.id).scalar())
                })

            return jsonify({"message": "Eligible users data written to MongoDB"}), 200

        except Exception as e:
            raise

        finally:
            db.session.close()










