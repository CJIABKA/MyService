from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_crontab import Crontab


appF = Flask(__name__)
appF.config.from_object(Config)
db = SQLAlchemy(appF)
migrate = Migrate(appF, db)
login = LoginManager(appF)
login.login_view = 'login'
crontab = Crontab(appF)


from app import routes, models, errors, scheduledtasks
