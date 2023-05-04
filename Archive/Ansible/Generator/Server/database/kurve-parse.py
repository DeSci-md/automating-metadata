from flask import Flask, jsonify, request
import requests
import psycopg2
import lightkurve as lk
import matplotlib.pyplot as plt
from thirdweb import ThirdwebSDK

# Flask Initialisation
app = Flask(__name__)

# Lightcurve initialisation 
planetTic = ""

# Contract Initialisation
sdk = ThirdwebSDK("mumbai")
contract = sdk.get_contract("0xed6e837Fda815FBf78E8E7266482c5Be80bC4bF9")
_receiver = ""
_tokenId = 0
_quantity = 0
data = contract.call("claim", 0xCdc5929e1158F7f0B320e3B942528E6998D8b25c, 2, 1)

# Flask/api routes
@app.route('/planet')
def planet():
    return jsonify({'planet' : 'planet'})

@app.post('/select_planet')
def select_planet():
    data = request.get_json()
    planetId = data['planetId']
    planetName = data['planetName']
    planetTic = data['planetTic']
    sector_data = lk.search_lightcurve(planetTic, author = 'SPOC', sector = 23)
    #lc = sector_data.download()
    #lc.plot()
    return sector_data

# Show planet data on frontend
@app.post('/show_planet') # Can we do some calculation for nft revealing using this (i.e. mint nft after classification)
def show_tic():
    lc = sector_data.plot()
    return lc

@app.post('/mint-planet')
def mint_planet():
    data = request.get_json()
    _receiver = data['profileAddress']
    _tokenId = data['tokenId']
    _quantity = 1
    data = contract.call("claim", _receiver, _tokenId, _quantity)

app.run(host='0.0.0.0', port=8080)