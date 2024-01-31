 # main file of the applicaiton

from flask import Flask
from config import Config
from models.User_info import db, User_info
from flask_migrate import Migrate
from Seeders.UserSeeder import UserSeeder  # Adjust the import statement



# from routes.api_routes import api_routes


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)


# app.register_blueprint(api_routes)
# app.register_blueprint(api_routes, url_prefix='/api')




if __name__ == '__main__':
    with app.app_context():
        # Run the seeder
        UserSeeder.run()
