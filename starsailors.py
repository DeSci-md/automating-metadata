from flask import Blueprint, request, jsonify
import numpy as np
import pandas as pd
import lightkurve as lk
import faiss

lightkurve_vector_bp = Blueprint('lightkurve_vector', __name__)

# Load example data
tpf = lk.search_targetpixelfile("KIC 11615890", quarter=3).download()
lc = tpf.to_lightcurve().flatten()

# Create the Faiss index
d = 4  # Number of dimensions (4D light curve)
index = faiss.IndexFlatL2(d)

# Convert the light curve to a 4D vector representation
vector = np.array([lc.time.mean(), lc.time.ptp(), lc.flux.mean(), lc.flux.ptp()]).astype('float32')

# Add the vector to the index
index.add(np.expand_dims(vector, 0))

# Define the route for receiving new classifications
@lightkurve_vector_bp.route('/classify', methods=['POST'])
def classify():
    # Get the data from the POST request
    data = request.get_json()
    # ping github/signal-k/sytizen

    # Convert the classification to a 1D vector
    classification = np.array([data['period'], data['duration'], data['depth'], data['transit_time']]).astype('float32')

    # Search for the nearest neighbor in the Faiss index
    distances, indices = index.search(np.expand_dims(classification, 0), k=1)

    # Store the classification in a Pandas DataFrame
    df = pd.DataFrame({'period': [classification[0]], 'duration': [classification[1]], 'depth': [classification[2]], 'transit_time': [classification[3]], 'index': [indices[0][0]]})

    # Save the DataFrame to disk (or update an existing file)
    df.to_csv('classifications.csv', index=False, mode='a', header=not os.path.exists('classifications.csv'))

    # Return a response to the client
    return jsonify({'status': 'success'})
