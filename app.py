# Imports
from flask import Flask, render_template, Blueprint, jsonify
import os
from supabase import create_client

# Initialisation
app = Flask(__name__)

# Flask blueprints
from search_flask import search_bp
from starsailors import lightkurve_vector_bp

# Base routes
@app.route('/')
def index():
    return "Hello World!"

# Running
if __name__ == "__main__":
    app.run()