# This package allows servers, requests, urls, etc.
from flask import Flask, request, render_template, redirect, url_for
# Create app var from Flask package
app = Flask(__name__)

# This packages allows for saving files to app dir
import os
import pandas as pd

# Set path to upload csv (path of current app dirname)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Create get route, function to run on request
@app.route('/')
def home_route():
    return render_template('upload.html')

# Create post & get route, function to run on request
@app.route('/results', methods=['POST', 'GET'])
def send_csv():
    if request.method == 'POST':
        if request.files['file'].filename == '' or request.files['file'].filename.endswith('.csv') == False:
            return redirect(url_for("home_route"))
        else:
            target = os.path.join(APP_ROOT, 'static/uploads')
            file = request.files['file']
            filename = file.filename
            destination = "/".join([target, filename])
            file.save(destination)
            df = pd.read_csv(destination)
            print(df)
            # df.columns = ['column_1','column_2','column_3','column_4','column_5']
            csvfinal = df
            os.remove(destination)
            csvfinal.to_csv(target + '/updated_file.csv', index=False)
            return render_template('results.html')
    else:
            return redirect(url_for("home_route"))

# This runs the server (provided by Flask)
if __name__ == '__main__':
    app.run(debug=True)
