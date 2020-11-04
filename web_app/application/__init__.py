from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application import config
#from flask_migrate import Migrate

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=config.username,
    password=config.password,
    hostname=config.hostname,
    databasename=config.databasename,
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
#migrate = Migrate(app, db)

from application import routes, routes_dev
