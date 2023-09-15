"""
Script for extracting machine readable text from a web publication/paper which
needs to be downloaded
Adapted from the process described by Wang et. al. 2022 10.1038/s41524-021-00687-2

Crossref API info: https://api.crossref.org/swagger-ui/index.html

habanero package info: https://pypi.org/project/habanero/
"""
import time  # for using time.sleep() if needing to pause data requests
from habanero import Crossref
from habanero import cn


cr = Crossref()

# Setting info for mailto for contact email and user-agent for description of use case
# For attempts to get into the 'polite pool' for paper requests through the API
cr.mailto = 'haloh@mix.wvu.edu'
cr.ua_string = 'Python script for retrieving paper info from query for research.'

# query section, request results based on a search
# cursor='*' alloy 'deep paging' (according to function documentation in crossref.py)
# cursor_max sets the max number of records to retrieve, by default it's 20 I think
# seems to do max results returned from deep paging in sets of 20, e.g. a request of 15 still gives 20
n = 2  # multiple of 20 for deep paging
request = cr.works(query = "Automated pipeline for superalloy data by text mining", cursor='*', cursor_max=n*20, progress_bar=True)  # test query searching for papers based on a string

allowed_types = ['proceedings-article', 'book-chapter', 'dissertation', 'journal-article']  # specifying document types of parse
# print the title and the type of item from the results
for i in range(n):
    for j in range(len(request[i]['message']['items'])):
        if request[i]['message']['items'][j]['type'] not in allowed_types:  # skipping if not a type wanted
            continue
        title = request[i]['message']['items'][j]['title'][0]
        type = request[i]['message']['items'][j]['type']
        print(f'{title}, {type}')  # print the title and type of each results
        time.sleep(0.25)  # sleep between prints so it's not too fast


request_doi = cr.works(ids = '10.1038/s41524-021-00687-2')  # search for a specific paper using a DOI number
print(request_doi['message']['title'][0])
citation = cn.content_negotiation(ids = '10.1038/s41524-021-00687-2', format = 'text')  # get citation for the DOI
print(citation)
