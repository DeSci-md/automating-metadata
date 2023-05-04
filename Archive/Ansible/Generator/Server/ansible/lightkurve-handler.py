from flask import Flask, Blueprint
from random import randint, randrange
import lightkurve as lk

lightkurve_compose = Blueprint('lightkurve-compose', __name__)

def generate_random_number():
    fixed_digits = 8
    randomNumber = random.randrange(11111111, 99999999, fixed_digits)

@lightkurve_compose.route('/generate', methods=['GET', 'POST'])
def generate_random_tic():
    generate_random_number()
    sector_data = lk.search_lightcurve(randomNumber, author = 'SPOC', sector = 18)
    # add try catch block -> if sector_data cannot be set, regenerate a random number

@lightkurve_compose.route('/generate-sector-data', methods=['GET', 'POST'])
def generate_sector_data():
    selected_id = random.choice(['TIC 55525572', 'TIC 284475976'])
    sector_data = lk.search_lightcurve(selected_id)#, author = 'SPOC', sector = 23)
    sector_data # Take first item exptime, if > value, increase radius in generator
    #lc = sector_data.plot()
    #lc.plot()