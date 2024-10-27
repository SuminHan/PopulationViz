from io import StringIO
import urllib.parse
import json
import sys
import pandas as pd
import geopandas as gpd
import os
import numpy as np
import datetime
from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


#app = Flask(__name__)

### initialization
#with open('../lte_cell_square.geojson') as fp:
#    lte_gdf = json.load(fp)
#lte_gdf = gpd.read_file('../lte_cell_square.geojson')

bgdf = gpd.read_file('local_people_area.geojson')
sgdf = gpd.read_file('seoul_link_network.geojson')


tdir = '/4TBSSD/TRAFFIC_DATASET/LOCAL_PEOPLE_NPY/'
mdir = '/4TBSSD/TRAFFIC_DATASET/TRAFFIC_SPEED_NPY/'
fnames = sorted(os.listdir(tdir))
arr = np.load(os.path.join(tdir, fnames[0]))

bgdf['height'] = arr[:, 19]/bgdf['area']*10000


@app.route("/living")
def hello():
    return bgdf.__geo_interface__

@app.route("/data")
def data():
    ymd = request.args.get('ymd', default = '20180301', type = str)
    hour = request.args.get('hour', default = 9, type = int)
    y = int(ymd[:4])
    m = int(ymd[4:6])
    d = int(ymd[6:])
    oneday = datetime.timedelta(days=1)
    mdate = datetime.date(y, m, d)
    if hour > 24:
        mdate += oneday
    larr = np.load(os.path.join(tdir, '{:04d}{:02d}{:02d}.npy'.format(mdate.year,mdate.month,mdate.day)))
    tarr = np.load(os.path.join(mdir, '{:04d}{:02d}{:02d}.npy'.format(mdate.year,mdate.month,mdate.day)))
    ldict = {i:v for i, v in zip(bgdf['TOT_REG_CD'].tolist(), larr[:, hour%24])}
    tdict = {i:v for i, v in zip(sgdf['LINK_ID'].tolist(), tarr[:, hour%24])}
    alldict = dict()
    alldict['lte'] = ldict
    alldict['traf'] = tdict
    return json.dumps(alldict)


@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    context = ('/etc/apache2/ucert/crystal.kaist.ac.kr.crt', '/etc/apache2/ucert/crystal.kaist.ac.kr.key')  # Path to your .crt and .key files
    app.run(host="crystal.kaist.ac.kr", port=15151, ssl_context=context)
