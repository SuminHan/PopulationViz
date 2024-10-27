from io import StringIO
import urllib.parse
import json
import sys
import pandas as pd
import geopandas as gpd
import os
import numpy as np
import datetime
from flask import Flask, render_template, request, send_file
from flask_cors import CORS

app = Flask(__name__, static_folder='assets', static_url_path='/assets')
CORS(app)

bgdf = gpd.read_file('assets/population_grid_128x128_points_filtered.geojson')

popu_df = pd.read_csv('assets/population_grid_128x128_data_light.csv', index_col=0)
popu_df.index = pd.to_datetime(popu_df.index)


@app.route("/living")
def living():
    return bgdf.__geo_interface__

@app.route("/data")
def data():
    ymd = request.args.get('ymd', default = '20170301', type = str)
    hour = request.args.get('hour', default = 9, type = int)
    print(ymd, hour)
    y = int(ymd[:4])
    m = int(ymd[4:6])
    d = int(ymd[6:])
    oneday = datetime.timedelta(days=1)
    mdate = datetime.datetime(y, m, d, hour%24)
    if hour > 24:
        mdate += oneday
        
    ldict = dict(popu_df.loc[mdate])
    alldict = dict()
    alldict['lte'] = ldict
    return alldict


@app.route("/")
def main():
    return send_file('templates/population.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
