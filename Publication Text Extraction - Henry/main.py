"""
Script for extracting machine readable text from a web publication/paper which
needs to be downloaded
Adapted from Wang et. al. 2022 10.1038/s41524-021-00687-2

Crossref API info: https://api.crossref.org/swagger-ui/index.html

habanero package info: https://pypi.org/project/habanero/

"""
import time  # for using time.sleep() if needing to pause data requests
from habanero import Crossref


cr = Crossref()

# query
x = cr.works(query = "ecology")
x['message']
x['message']['total-results']
x['message']['items']