# from flask.cli import AppGroup
# from models.UserInfo import db, UserInfo
# from faker import Faker
#
# seed_cli = AppGroup('seed', help="Seed the database with user information data.")
#
# @seed_cli.command('user_seeder')
# def seed_users():
#     """Seed the database with sample user data."""
#     fake = Faker()
#     try:
#         for _ in range(20):
#             user_info = {
#                 'name': fake.name(),
#                 'email': fake.email(),
#                 'age': fake.random_int(min=18, max=99),
#                 'password': fake.password(),
#             }
#             user = UserInfo(**user_info)
#             db.session.add(user)
#             db.session.commit()
#             print(f"User seeded: {user}")
#     except Exception as e:
#         db.session.rollback()
#         print(f"Error seeding users: {e}")
#     finally:
#         db.session.close()
#
#     print("Seeder executed successfully.")
