from flask import Flask
from config import ConfigMysql, ConfigMongoDB
from models.UserInfo import db, UserSpending, UserInfo
from flask_migrate import Migrate
from Seeders.UserSeeder import UserSeeder
from routes.api_routes import api_routes
from pymongo import MongoClient





app = Flask(__name__)

# Mysql Configuration
app.config.from_object(ConfigMysql)
db.init_app(app)
migrate = Migrate(app, db)


# MongoDB configuration
app.config.from_object(ConfigMongoDB)
mongo_client = MongoClient(app.config['MONGO_URI'])
mongo_db = mongo_client.get_database()

# routes
app.register_blueprint(api_routes, url_prefix='/api')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        UserSeeder.run()
    app.run(debug=True)
