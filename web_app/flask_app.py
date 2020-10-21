from flask import Flask, request, render_template
# get data
from flask import Flask
import pandas as pd
import pandas_datareader as pdr
#import numpy as np
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["DEBUG"] = True

pd.options.display.max_colwidth = -1

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="usuername",
    password="password",
    hostname="hostname",
    databasename="databasename",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text'].encode('unicode-escape').decode()
    #processed_text = text.upper()

    df = pd.read_sql('select `Subheader 1`, `Section Index`, site from corpusthomisticum where Content REGEXP "' + text + '"', con = db.engine)
    df = df.rename(columns = {'Subheader 1':'Work', 'Section Index':'Passage', 'site':'Site'})
    df['Site'] = df['Site'] + "#" + df['Passage'].str.extract(r'\[([0-9]+)\]')
    df['Passage'] = '<a href="' + df['Site'] + '" target="_blank">' + df['Passage'] + '</a>'
    #lt = df.values.tolist()
    #lt = list(map(str, lt))
    #print(lt)
    #return 1
    size = df['Passage'].size
    searchTerm = text
    return render_template('CorpThomOutput.html', tables=[df.to_html(classes='data', index = False, escape = False)], titles=df.columns.values, searchTerm = searchTerm, size = size)
