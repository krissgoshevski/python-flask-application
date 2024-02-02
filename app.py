from flask import Flask
from config import ConfigMysql
# from config import ConfigMysql, ConfigMongoDB
from models.UserInfo import db, UserSpending, UserInfo
from flask_migrate import Migrate
from Seeders.UserSeeder import UserSeeder
from routes.api_routes import api_routes


# from flask_mongoengine import MongoEngine
# from models.UserInfo import db as mysql_db, UserSpending, UserInfo
# from flask_mongoengine import Flask, MongoEngine, JSONEncoder



app = Flask(__name__)
app.config.from_object(ConfigMysql)
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(api_routes, url_prefix='/api')



# Mysql Configuration
# app.config.from_object(ConfigMysql)
# mysql_db.init_app(app)
# migrate = Migrate(app, mysql_db)



# MongoDB configuration
# app.config.from_object(ConfigMongoDB)
# mongo_db = MongoEngine(app)





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # mysql_db.create_all()
        UserSeeder.run()
    app.run(debug=True)
