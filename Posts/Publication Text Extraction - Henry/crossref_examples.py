"""
Examples and guide for usage of the crossref api through the habanero python
package.

Crossref API info: https://api.crossref.org/swagger-ui/index.html
habanero package info: https://pypi.org/project/habanero/
"""
import time  # for using time.sleep() if needing to pause data requests

from habanero import Crossref  # for obtaining paper DOI's, other info from searching
from habanero import cn


#%% Use of habanero package to extract data from Crossref database
cr = Crossref()  # define crossref object

# Setting info for mailto for contact email and user-agent for description of use case
# For attempts to get into the 'polite pool' for paper requests through the API
cr.mailto = 'haloh@mix.wvu.edu'
cr.ua_string = 'Python script for retrieving paper info from query for research.'

# query section, request results based on a search
# cursor='*' alloy 'deep paging' (according to function documentation in crossref.py)
# cursor_max sets the max number of records to retrieve, by default it's 20 I think
# seems to do max results returned from deep paging in sets of 20, e.g. a request of 15 still gives 20
n = 3  # multiple of 20 for deep paging
request = cr.works(query = "electrohydrodynamic printing ring electrode", cursor='*', cursor_max=n*20, progress_bar=True)  # test query searching for papers based on a string

# allowed_types = ['proceedings-article', 'book-chapter', 'dissertation', 'journal-article']  # specifying document types of parse
allowed_types = ['journal-article']

# Generate a list of parsed results
parsed_results = []
for i in range(n):
    for j in range(len(request[i]['message']['items'])):  # cycle through all the results obtained
        if request[i]['message']['items'][j]['type'] not in allowed_types:  # skipping if not a type wanted
            continue
        
        # print the title, publisher, and year for each result
        title = request[i]['message']['items'][j]['title'][0]
        journal = request[i]['message']['items'][j]['container-title']
        year = request[i]['message']['items'][j]['published']['date-parts'][0][0]
        print(f'{title}, {journal}, {year}')  # print the title and type of each results
        print("")


#%% Searching for a paper based on DOI
request_doi = cr.works(ids = '10.1038/s41524-021-00687-2')  # search for a specific paper using a DOI number
print(request_doi['message']['title'][0])


#%% Retrieving the citation info for a paper through the DOI
citation = cn.content_negotiation(ids = '10.1038/s41524-021-00687-2', format = 'text')  # get citation for the DOI
print(citation)