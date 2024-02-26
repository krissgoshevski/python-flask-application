from models.UserInfo import db, UserInfo
from faker import Faker

class UserSeeder:
    @staticmethod
    def run():
        fake = Faker()
        for _ in range(20):
            user_info = {
                'name': fake.name(),
                'email': fake.email(),
                'age': fake.random_int(min=18, max=99),
                'password': fake.password(),
            }
            user = UserInfo(**user_info)
            db.session.add(user)

        db.session.commit()