import pandas as pd 
import numpy as np
import matplotlib.pyplot as plot

import os 
import uuid

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = 'uploads'

df = None #global dataframes variable 


#for the user to upload a CSV file
@app.route("/", methods=["GET","POST"])
def index():
    global df
    if request.method == "POST":
        file = request.files['file']
        if file.filename.endswith('.csv'):
            filePath  =  os.path.join(app.config["UPLOAD_FOLDER"],file.filename)
            file.save(filePath)
            df = pd.read_csv(filePath)
            return redirect(url_for("display_data"))
    return render_template('index.html')

#for displaying the uploaded file in html table 
@app.route("/display")
def display_data():
    global df 
    if df is None:
        return redirect(url_for("index"))
    return render_template("display.html", tables = [df.to_html(classes='data')], titles = df.columns.values)

#for processing the data
@app.route("/process/<action>")
def process_data(action):
    global df
    if df is None:
        return redirect(url_for('index'))
    
    if action == "fill_with_zero":
        df =  df.fillna(0)
    elif action =="fill_mean":
        df = df.fillna(df.mean(numeric_only=True))
    elif action == "drop":
        df = df.dropna()

    return redirect(url_for("display_data"))

if __name__ == "__main__":
    os.makedirs("uploads",exist_ok=True)
    app.run(debug=True)