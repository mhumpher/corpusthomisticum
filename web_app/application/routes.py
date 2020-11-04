from application import app , db
from flask import Flask, request, render_template
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import re

pd.options.display.max_colwidth = -1

@app.route('/')
def hello_world():
    return render_template('corpus_thomisticum_home.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text'].encode('unicode-escape').decode()
    #processed_text = text.upper()

    df = pd.read_sql('select `Subheader 1`, `Section Index`, site, Content from corpusthomisticum where Content REGEXP "' + text + '"', con = db.engine)
    df = df.rename(columns = {'Subheader 1':'Work', 'Section Index':'Passage', 'site':'Site'})
    df['Site'] = df['Site'] + "#" + df['Passage'].str.extract(r'\[([0-9]+)\]')
    df['Passage'] = '<a href="' + df['Site'] + '" target="_blank">' + df['Passage'] + '</a>'
    df['Selection'] = "..." + df['Content'].str.extract(r"(.{0,50}" + text + r".{0,50})", flags = re.IGNORECASE) + "..."
    df = df.drop(['Content', 'Site'],axis = 1)
    #lt = df.values.tolist()
    #lt = list(map(str, lt))
    #print(lt)
    #return 1
    size = df['Passage'].size
    searchTerm = text
    return render_template('corpus_thomisticum_output.html', tables=[df.to_html(classes='data', index = False, escape = False, justify = 'center')], titles=df.columns.values, searchTerm = searchTerm, size = size)
