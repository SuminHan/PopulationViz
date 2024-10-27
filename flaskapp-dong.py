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

#app = Flask(__name__)
app = Flask(__name__, static_folder='assets', static_url_path='/assets')
CORS(app)


#app = Flask(__name__)

### initialization
#with open('../lte_cell_square.geojson') as fp:
#    lte_gdf = json.load(fp)
#lte_gdf = gpd.read_file('../lte_cell_square.geojson')

bgdf = gpd.read_file('assets/local_people_area.geojson')
sgdf = gpd.read_file('assets/seoul_link_network.geojson')


# tdir = '/4TBSSD/TRAFFIC_DATASET/LOCAL_PEOPLE_NPY/'
# mdir = '/4TBSSD/TRAFFIC_DATASET/TRAFFIC_SPEED_NPY/'
# fnames = sorted(os.listdir(tdir))
# arr = np.load(os.path.join(tdir, fnames[0]))
# bgdf['height'] = arr[:, 19]/bgdf['area']*10000
#popu_df = pd.concat([
    #pd.read_csv('../newdata2/population_data_2017.csv', index_col=0),
    #pd.read_csv('../newdata2/population_data_2018.csv', index_col=0),
    #pd.read_csv('../newdata2/population_data_2019.csv', index_col=0),
    #pd.read_csv('../newdata2/population_data_2020.csv', index_col=0)
#])
#traf_df = pd.concat([
    #pd.read_csv('../newdata2/traffic_data_2017.csv', index_col=0),
    #pd.read_csv('../newdata2/traffic_data_2018.csv', index_col=0),
    #pd.read_csv('../newdata2/traffic_data_2019.csv', index_col=0),
    #pd.read_csv('../newdata2/traffic_data_2020.csv', index_col=0)
#])
    
#vol_df = pd.concat([
    #pd.read_csv('../newdata2/volume_data_2017.csv', index_col=0),
    #pd.read_csv('../newdata2/volume_data_2018.csv', index_col=0),
    #pd.read_csv('../newdata2/volume_data_2019.csv', index_col=0),
    #pd.read_csv('../newdata2/volume_data_2020.csv', index_col=0)
#])

popu_df = pd.read_csv('population_data_2018.csv', index_col=0)
traf_df = pd.read_csv('traffic_data_2018.csv', index_col=0)
vol_df  = pd.read_csv('volume_data_2018.csv', index_col=0)
popu_df = popu_df.fillna(0)
traf_df = traf_df.fillna(0)
vol_df  = vol_df.fillna(0)
popu_df.index = pd.to_datetime(popu_df.index)
traf_df.index = pd.to_datetime(traf_df.index)
vol_df.index  = pd.to_datetime(vol_df.index)


@app.route("/living")
def living():
    return bgdf.__geo_interface__
@app.route("/link")
def link():
    return sgdf.__geo_interface__

@app.route("/data")
def data():
    ymd = request.args.get('ymd', default = '20180301', type = str)
    hour = request.args.get('hour', default = 9, type = int)
    print(ymd, hour)
    y = int(ymd[:4])
    m = int(ymd[4:6])
    d = int(ymd[6:])
    oneday = datetime.timedelta(days=1)
    mdate = datetime.datetime(y, m, d, hour%24)
    if hour > 24:
        mdate += oneday    
    #larr = np.load(os.path.join(tdir, '{:04d}{:02d}{:02d}.npy'.format(mdate.year,mdate.month,mdate.day)))
    #tarr = np.load(os.path.join(mdir, '{:04d}{:02d}{:02d}.npy'.format(mdate.year,mdate.month,mdate.day)))
    ldict = dict(popu_df.loc[mdate]) #{i:v for i, v in zip(bgdf['TOT_REG_CD'].tolist(), larr[:, hour%24])}
    tdict = dict(traf_df.loc[mdate]) #{i:v for i, v in zip(sgdf['LINK_ID'].tolist(), tarr[:, hour%24])}
    #print(ldict, tdict)
    alldict = dict()
    alldict['lte'] = ldict
    alldict['traf'] = tdict
    return alldict


@app.route("/")
def main():
    #return render_template('traffic-population.html')
    return send_file('templates/traffic-population.html')


@app.route("/population")
def main_population():
    return send_file('templates/population.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=15151)
