from flask import Blueprint, request
from moralis import auth
from flask_cors import CORS

moralis_handler = Blueprint('moralis_handler', __name__)

# Moralis setup
apiKey = "kJfYYpmMmfKhvaWMdD3f3xMMb24B4MHBDDVrfjslkKgTilvMgdwr1bwKUr8vWdHH" # Move to env

# Authentication routes -> move to auth.py later
# Request a challenge when a user attempts to connect their wallet
@moralis_handler.route('/requestChallenge', methods=['GET'])
def reqChallenge():
    args = request.args # Fetch the arguments from the request

    # Get request body -> compare with data from Moralis
    body = {
        "domain": "sailors.skinetics.tech",
        "chainId": args.get("chainId"),
        "address": args.get("address"),
        "statement": "Please confirm authentication by signing this transaction",
        "uri": "https://ipfs.skinetics.tech/auth/1...",
        "expirationTime": "2023-01-01T00:00:00.000Z",
        "notBefore": "2020-01-01T00:00:00.000Z",
        "resources": ['https://docs.skinetics.tech/crypto/auth/signing'],
        "timeout": 30,
    }

    # Deliver the result to Moralis client
    result = auth.challenge.request_challenge_evm(
        api_key=apiKey,
        body=body,
    )

    return result

# Verify signature from user
@moralis_handler.route('/verifyChallenge', methods=['GET'])
def verifyChallenge():
    args = request.args

    body = { # Request body
        "message": args.get("message"),
        "signature": args.get("signature"),
    },

    result = auth.challenge.verify_challenge_evm(
        api_key=apiKey,
        body=body,
    ),

    return result