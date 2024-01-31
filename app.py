from flask import Flask
from config import Config
from models.UserInfo import db, UserSpending, UserInfo
from flask_migrate import Migrate
from Seeders.UserSeeder import UserSeeder
from routes.api_routes import api_routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(api_routes)



@app.route('/', methods=['GET'])
def index():
    return 'test'



if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Run the seeder
        UserSeeder.run()

    app.run(debug=True)
