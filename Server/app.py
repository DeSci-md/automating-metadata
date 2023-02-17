from flask import Flask, request, make_response, jsonify, Blueprint
from datetime import datetime, timedelta

"""# Jupyter interaction
import io, os, sys, types # https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import Interactiveshell"""

# Flask blueprints/routes
from auth.moralisHandler import moralis_handler
from contracts.planetDrop import planet_drop
from database.connection import database_connection
# from database.unity-integration import unity_database_connection
# from ansible.tic_classify import tic_classify
# from ansible.classify import lightkurve_handler

app = Flask(__name__)
app.register_blueprint(moralis_handler, url_prefix='/moralis-auth')
app.register_blueprint(planet_drop, url_prefix='/planets')
app.register_blueprint(database_connection, url_prefix='/database')
# app.register_blueprint(unity-database_connection, url_prefix='/database-unity')
# app.register_blueprint(tic_classify, url_prefix='/lightkurve')
# app.register_blueprint(lightkurve__handler, url_prefix='/lightkurve-handle')

@app.route('/')
def index():
    return "Hello World"