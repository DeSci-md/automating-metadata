from flask import Blueprint, request
from thirdweb import ThirdwebSDK

planet_drop = Blueprint('planet_drop', __name__)

# Get NFT balance for Planet Edition Drop (https://thirdweb.com/goerli/0xdf35Bb26d9AAD05EeC5183c6288f13c0136A7b43/code)
@planet_drop.route('/balance')
def get_balance():
    # Planet Edition Drop Contract
    network = "goerli"
    sdk = ThirdwebSDK(network)
    contract = sdk.get_edition_drop("0xdf35Bb26d9AAD05EeC5183c6288f13c0136A7b43")

    address = "0xCdc5929e1158F7f0B320e3B942528E6998D8b25c"
    token_id = 0
    balance = contract.balance_of(address, token_id)
    
    return str(balance)

@planet_drop.route('/get_planet')
def get_planet():
    network = 'goerli'
    sdk = ThirdwebSDK(network)

    # Getting Planet (candidate nfts)
    contract = sdk.get_contract("0x766215a318E2AD1EbdC4D92cF2A3b70CBedeac31")
    tic55525572 = contract.call("uri", 0) # For token id 0, tic id 55525572
    return str(tic55525572)

@planet_drop.route('/mint_planet', methods=["GET", "POST"])
def create_planet():
    #Output from IPFS gateway: #{"name":"TIC 55525572","description":"Exoplanet candidate discovered by TIC ID. \n\nReferences: https://exoplanets.nasa.gov/exoplanet-catalog/7557/toi-813-b/\nhttps://exofop.ipac.caltech.edu/tess/target.php?id=55525572\n\nDeepnote Analysis: https://deepnote.com/workspace/star-sailors-49d2efda-376f-4329-9618-7f871ba16007/project/Star-Sailors-Light-Curve-Plot-b4c251b4-c11a-481e-8206-c29934eb75da/%2FMultisector%20Analysis.ipynb","image":"ipfs://Qma2q8RgX1X2ZVcfnJ7b9RJeKHzoTXahs2ezzqQP4f5yvT/0.png","external_url":"","background_color":"","attributes":[{"trait_type":"tic","value":"55525572"},{"trait_type":"mass_earth","value":"36.4"},{"trait_type":"type","value":"neptune-like"},{"trait_type":"orbital_period","value":"83.9"},{"trait_type":"eccentricity","value":"0.0"},{"trait_type":"detection_method","value":"transit"},{"trait_type":"orbital_radius","value":"0.423"},{"trait_type":"radius_jupiter","value":"0.599"},{"trait_type":"distance_earth","value":"858"}]}
    # Multiple instances for the same ID will be created (as long as the traits are the same), one for each person, as each planet instance appeared differently and will be manipulated differently by users
    # Creating a planet nft based on discovery
    network = 'goerli'
    sdk = ThirdwebSDK(network)
    contract = sdk.get_contract("0x766215a318E2AD1EbdC4D92cF2A3b70CBedeac31")
    #data = contract.call("lazyMint", _amount, _baseURIForTokens, _data) (POST data)
    # Interaction flow -> https://www.notion.so/skinetics/Sample-Planets-Contract-4c3bdcbca4b9450382f9cc4e72e081f7

"""
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
"""