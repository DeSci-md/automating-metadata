from flask import Blueprint, request
from thirdweb.types import LoginPayload
from thirdweb import ThirdwebSDK
from datetime import datetime, timedelta
import os

thirdweb_handler = Blueprint('thirdweb_handler', __name__)

# Getting proposals
web3Sdk = ThirdwebSDK("goerli")
contract = web3Sdk.get_contract("0xCcaA1ABA77Bae6296D386C2F130c46FEc3E5A004")
proposals = contract.call("getProposals")

# Minting candidate nfts
nftSdk = ThirdwebSDK('mumbai')
nftContract = nftSdk.get_contract("0xed6e837Fda815FBf78E8E7266482c5Be80bC4bF9")

@thirdweb_handler.route('/login', methods=['POST'])
def login():
    private_key = os.environ.get("PRIVATE_KEY")
    
    if not private_key:
        print("Missing PRIVATE_KEY environment variable")
        return "Wallet private key not set", 400

    sdk = ThirdwebSDK.from_private_key(private_key, 'mumbai') # Initialise the sdk using the wallet and on mumbai testnet chain
    payload = LoginPayload.from_json(request.json['payload'])

    # Generate access token using signed payload
    domain = 'sailors.skinetics.tech'
    token = sdk.auth.generate_auth_token(domain, payload)

    res = make_response()
    res.set_cookie(
        'access_token',
        token,
        path='/',
        httponly=True,
        secure=True,
        samesite='strict',
    )
    return res, 200

@thirdweb_handler.route('/authenticate', methods=['POST'])
def authenticate():
    private_key = os.environ.get("PRIVATE_KEY")
    
    if not private_key:
        print("Missing PRIVATE_KEY environment variable")
        return "Wallet private key not set", 400

    sdk = ThirdwebSDK.from_private_key(private_key, 'mumbai')

    # Get access token from cookies
    token = request.cookies.get('access_token')
    if not token:
        return 'Unauthorised', 401
    
    domain = 'sailors.skinetics.tech'

    try:
        address = sdk.auth.authenticate(domain, token)
    except:
        return "Unauthorized", 401
    
    print(jsonify(address))
    return jsonify(address), 200

@thirdweb_handler.route('/logout', methods=['POST'])
def logout():
    res = make_response()
    res.set_cookie(
        'access_token',
        'none',
        expires=datetime.utcnow() + timedelta(second = 5)
    )
    return res, 200

@thirdweb_handler.route('/proposals', methods=["GET", "POST"])
def getProposals():
    # Mint nft based on proposal id
    proposalCandidate = nftContract.call("lazyMint", _amount, _baseURIForTokens, _data) # Get this from Jupyter notebook -> https://thirdweb.com/mumbai/0xed6e837Fda815FBf78E8E7266482c5Be80bC4bF9/nfts token id 0 (e.g.)
    createProposal = contract.call("createProposal", _owner, _title, _description, _target, _deadline, _image) # Get this from PUSH req contents

    return proposals