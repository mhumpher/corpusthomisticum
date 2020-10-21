from flask import Flask
import pandas as pd
import pandas_datareader as pdr
import numpy as np
from datetime import datetime
import pandas
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
app = Flask(__name__)
app.config["DEBUG"] = True


SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="username",
    password="password",
    hostname="hostname",
    databasename="databasename",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

df = pd.read_csv("corp_out.csv")
dtype = {
    "Content": LONGTEXT
    }
df.to_sql(name = 'corpusthomisticum', con = db.engine, index = False, if_exists = 'replace', chunksize = 1000, dtype= dtype)
