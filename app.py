import pandas as pd 
import numpy as np
import matplotlib.pyplot as plot

import os 
import uuid

from flask import Flask, render_template, request, send_file

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = 'uploads'
app.config["STACK_FOLDER"] ="stack"

original_df = None #global dataframes variable 
modified_df = None

#for the user to upload a CSV file
@app.route("/", methods=["GET","POST"])
def index():
    global original_df, modified_df

    if request.method == "POST":
        file = request.files["file"]
        if file.filename.endswith(".csv"):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            original_df = pd.read_csv(filepath)
            modified_df = original_df.copy()  # keep a modifiable version

    table_html = None
    if modified_df is not None:
        table_html = modified_df.to_html(classes="data")

    return render_template("index.html", table=table_html)
#for displaying the uploaded file in html table 
# @app.route("/display")
# def display_data():
#     global df 
#     if df is None:
#         return redirect(url_for("index"))
#     return render_template("display.html", tables = [df.to_html(classes='data')], titles = df.columns.values)

#for processing the data
@app.route("/process/<action>")
def process_data(action):
    global original_df,modified_df

    if original_df is None:
        return render_template("index.html",table = None)
    
    df = original_df.copy()

    if action == "fill_with_zero":
        df =  df.fillna(0)
    elif action =="fill_mean":
        df = df.fillna(df.mean(numeric_only=True))
    elif action == "drop":
        df = df.dropna()

    modified_df =df


    return render_template('index.html',table= df.to_html(classes="data"))

@app.route("/download")
def download_data():
    global modified_df
    if modified_df is None:
        return render_template("index.html", table=None)

    filename = f"{app.config['UPLOAD_FOLDER']}/modified_{uuid.uuid4().hex}.csv"
    modified_df.to_csv(filename, index=False)
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    os.makedirs("uploads",exist_ok=True)
    app.run(debug=True)