from flask import Blueprint, request
from thirdweb import ThirdwebSDK
import matplotlib.pyplot as plt
import lightkurve as lk
from io import BytesIO
import base64
import os
from dotenv import load_dotenv
import psycopg2
from storage3 import create_client

tic_classify = Blueprint('tic_classify', __name__)

# Global variables (anomaly base stats)
tic = ''

# Database setup
load_dotenv()
url = os.getenv("DATABASE_URL")
storage_url = os.getenv("STORAGE_URL")
key = os.getenv("ANON_KEY")
headers = {"apiKey": key, 'Authorization': f"Bearer {key}"}
storage_client = create_client(storage_url, headers, is_async=False)
connection = psycopg2.connect(url)
# PostgreSQL queries -> see more at database/connection.py
CREATE_PLANETS_TABLE = (
    """CREATE TABLE IF NOT EXISTS planets (id SERIAL PRIMARY KEY, user_id INTEGER, temperature REAL, date TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);"""
)
INSERT_PLANET = (
    'INSERT INTO planets (user_id, temperature, date) VALUES (%s, %s, %s);'
)
"""CREATE_TIC_TABLE = ( # Link this with the main planets table -> create a new table with a foreign key ref
    #CREATE TABLE IF NOT EXISTS tic (tic_id SERIAL PRIMARY KEY, tic TEXT, planet_id INTEGER, FOREIGN KEY(planet_id) REFERENCES planets(id) ON DELETE CASCADE);
#)"""
CREATE_TIC_TABLE = (
    'CREATE TABLE IF NOT EXISTS tic (id SERIAL PRIMARY KEY, tic_id TEXT);'
)
INSERT_TIC = (
    'INSERT INTO tic (tic_id) VALUES (%s);'
)

@tic_classify.route('/ticId', methods=['GET', "POST"])
def ticId():
    TIC = 'TIC 284475976'
    sector_data = lk.search_lightcurve(TIC, author = 'SPOC', sector = 23)

    buf = BytesIO()
    sector_data.savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode("ascii") # embed result in html output
    return f"<img src='data:image/png;base64,{data}'/>"

@tic_classify.route('/search', methods=['GET', 'POST'])
def search():
    data = request.get_json()
    tic = data['ticid']
    
    sector_data = lk.search_lightcurve(tic, author = 'SPOC', sector = 18) # post tic & other request data to https://deepnote.com/workspace/star-sailors-49d2efda-376f-4329-9618-7f871ba16007/project/lightkurvehandler-dca7e16c-429d-42f1-904d-43898efb2321/

    # Connect to the database
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_PLANETS_TABLE)
            cursor.execute(CREATE_TIC_TABLE)
            cursor.execute(INSERT_TIC, (tic,))
            #tic_id = cursor.fetchone()[0]
            # Get the id of inserted row returned, send to Supabase
            

    sector_data = lk.search_lightcurve(tic, author = 'SPOC', sector = 18) # new bug discovered: https://www.notion.so/skinetics/Sample-Planets-Contract-4c3bdcbca4b9450382f9cc4e72e081f7#da4bef6caef746ac8017d6511ff7fb52
    #available_data_all = lk.search_lightcurve(tic, author = 'SPOC')
    #select_sectors = available_data_all[0:4]
    #lc_collection = select_sectors.download_all()

    lc = lk.search_lightcurve(tic, author='SPOC', sector=18).download()
    #lc = lc.remove_nans().remove_outliers()
    #lc.to_fits(path='lightcurve.fits')

    return(storage_client.list_buckets())