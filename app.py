# This package allows servers, requests, urls, etc.
from flask import Flask, request, render_template, redirect, url_for
# Create app var from Flask package
app = Flask(__name__)

# This packages allows for saving files to app dir
import os
from geopy.geocoders import GoogleV3
import pandas as pd
import folium
# Set path to upload csv (path of current app dirnae)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

geolocator = GoogleV3(api_key='AIzaSyCYNaAhybO8b6cO08LuYNLs2LZsmKDpaXc', domain='maps.googleapis.com', user_agent="geofindr_v1")

# Create get route, function to run on request
@app.route('/')
def home_route():
    return render_template('upload.html')

# Create post route, function to run on request
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
            df = pd.read_csv(destination,converters={'zip':str})
            df.columns = ['id','address','city','state','zip']
            latitudes = []
            longitudes = []
            m = folium.Map(location=[37, -95], tiles="OpenStreetMap", zoom_start=5)

            for index, row in df.iterrows():
                address = str(row['address'])
                city = str(row['city'])
                state = str(row['state'])
                zip = str(row['zip'])
                location = geolocator.geocode("{} {} {} {}".format(address, city, state, zip), timeout=10)
                if location == None:
                    latitudes.append('unknown')
                    longitudes.append('unknown')
                else:
                    latitudes.append(location.latitude)
                    longitudes.append(location.longitude)
                    folium.Marker(
                    location=[location.latitude, location.longitude],
                    icon=folium.Icon(color='red')
                    ).add_to(m)
            df['latitude'] = latitudes
            df['longitude'] = longitudes
            m.save('templates/store_map.html')
            csvfinal = df
            os.remove(destination)
            csvfinal.to_csv(target + '/updated_store_list.csv', index=False)
            return render_template('results.html')
    else:
            return redirect(url_for("home_route"))

@app.route('/map')
def map_route():
    return render_template('store_map.html')

# This runs the server (provided by Flask)
if __name__ == '__main__':
    app.run(debug=True)
