from flask import Flask
from config import ConfigMysql
from models.UserInfo import db, UserSpending, UserInfo
from flask_migrate import Migrate
from Seeders.UserSeeder import UserSeeder
from routes.api_routes import api_routes
from flask_cors import CORS

from flask_bcrypt import Bcrypt





app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# Mysql Configuration
app.config.from_object(ConfigMysql)
db.init_app(app)
migrate = Migrate(app, db)


# routes
app.register_blueprint(api_routes, url_prefix='/api')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        UserSeeder.run()
    app.run(debug=True)


