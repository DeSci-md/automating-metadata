"""
Script for extracting machine readable text from a web publication/paper which
needs to be downloaded
Adapted from the process described by Wang et. al. 2022 10.1038/s41524-021-00687-2

Crossref API info: https://api.crossref.org/swagger-ui/index.html
habanero package info: https://pypi.org/project/habanero/
Elsevier API info: https://dev.elsevier.com/documentation/FullTextRetrievalAPI.wadl
elsapy package info: https://github.com/ElsevierDev/elsapy/blob/master/exampleProg.py
"""
import json  # for reading in config file for elsevier API key
import time  # for using time.sleep() if needing to pause data requests

from habanero import Crossref  # for obtaining paper DOI's, other info from searching
from habanero import cn

# package importing based on exampleProg.py from the elsapy github
# for obtaining full text of publications
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch


#%% Use of habanero package to extract data from Crossref database
# cr = Crossref()  # define crossref object

# # Setting info for mailto for contact email and user-agent for description of use case
# # For attempts to get into the 'polite pool' for paper requests through the API
# cr.mailto = 'haloh@mix.wvu.edu'
# cr.ua_string = 'Python script for retrieving paper info from query for research.'

# # query section, request results based on a search
# # cursor='*' alloy 'deep paging' (according to function documentation in crossref.py)
# # cursor_max sets the max number of records to retrieve, by default it's 20 I think
# # seems to do max results returned from deep paging in sets of 20, e.g. a request of 15 still gives 20
# n = 5  # multiple of 20 for deep paging
# request = cr.works(query = "electrohydrodynamic printing ring electrode", cursor='*', cursor_max=n*20, progress_bar=True)  # test query searching for papers based on a string

# allowed_types = ['proceedings-article', 'book-chapter', 'dissertation', 'journal-article']  # specifying document types of parse
# # allowed_types = ['proceedings-article', 'journal-article']

# # print the title and the type of item from the results
# for i in range(n):
#     for j in range(len(request[i]['message']['items'])):
#         if request[i]['message']['items'][j]['type'] not in allowed_types:  # skipping if not a type wanted
#             continue
#         title = request[i]['message']['items'][j]['title'][0]
#         type = request[i]['message']['items'][j]['type']
#         print(f'{title}, {type}')  # print the title and type of each results
#         # time.sleep(0.25)  # sleep between prints so it's not too fast


# request_doi = cr.works(ids = '10.1038/s41524-021-00687-2')  # search for a specific paper using a DOI number
# print(request_doi['message']['title'][0])
# citation = cn.content_negotiation(ids = '10.1038/s41524-021-00687-2', format = 'text')  # get citation for the DOI
# print(citation)


#%% Use of elsapy for obtaining machine readable text from online publications
# load config/api key
with open("config.json") as file:
    config = json.load(file)
    api_key = config['apikey']


# Initialize client
client = ElsClient(api_key)

# # Author example
# # Initialize author with uri
# my_auth = ElsAuthor(uri = 'https://api.elsevier.com/content/author/author_id/7004367821')

# # Read author data
# if my_auth.read(client):  # returns True if the my_auth search comes back, otherwise is False
#     print ("my_auth.full_name: ", my_auth.full_name)
# else:
#     print ("Read author failed.")


# ## Affiliation example
# # Initialize affiliation with ID as string
# my_aff = ElsAffil(affil_id = '60101411')
# if my_aff.read(client):
#     print ("my_aff.name: ", my_aff.name)
#     my_aff.write()
# else:
#     print ("Read affiliation failed.")

# ## Scopus (Abtract) document example
# # Initialize document with ID as integer
# scp_doc = AbsDoc(scp_id = 84872135457)
# if scp_doc.read(client):
#     print ("scp_doc.title: ", scp_doc.title)
#     scp_doc.write()   
# else:
#     print ("Read document failed.")

# ## ScienceDirect (full-text) document example using PII
# pii_doc = FullDoc(sd_pii = 'S1674927814000082')
# if pii_doc.read(client):
#     print ("pii_doc.title: ", pii_doc.title)
#     pii_doc.write()   
# else:
#     print ("Read document failed.")

## ScienceDirect (full-text) document example using DOI
doi_doc = FullDoc(doi = '10.1038/s41524-021-00687-2')
if doi_doc.read(client):
    print ("doi_doc.title: ", doi_doc.title)
    doi_doc.write()   
else:
    print ("Read document failed.")


# ## Load list of documents from the API into affilation and author objects.
# # Since a document list is retrieved for 25 entries at a time, this is
# #  a potentially lenghty operation - hence the prompt.
# print ("Load documents (Y/N)?")
# s = input('--> ')

# if (s == "y" or s == "Y"):

#     ## Read all documents for example author, then write to disk
#     if my_auth.read_docs(client):
#         print ("my_auth.doc_list has " + str(len(my_auth.doc_list)) + " items.")
#         my_auth.write_docs()
#     else:
#         print ("Read docs for author failed.")

#     ## Read all documents for example affiliation, then write to disk
#     if my_aff.read_docs(client):
#         print ("my_aff.doc_list has " + str(len(my_aff.doc_list)) + " items.")
#         my_aff.write_docs()
#     else:
#         print ("Read docs for affiliation failed.")

# ## Initialize author search object and execute search
# auth_srch = ElsSearch('authlast(keuskamp)','author')
# auth_srch.execute(client)
# print ("auth_srch has", len(auth_srch.results), "results.")

# ## Initialize affiliation search object and execute search
# aff_srch = ElsSearch('affil(amsterdam)','affiliation')
# aff_srch.execute(client)
# print ("aff_srch has", len(aff_srch.results), "results.")

# ## Initialize doc search object using Scopus and execute search, retrieving 
# #   all results
# doc_srch = ElsSearch("AFFIL(dartmouth) AND AUTHOR-NAME(lewis) AND PUBYEAR > 2011",'scopus')
# doc_srch.execute(client, get_all = True)
# print ("doc_srch has", len(doc_srch.results), "results.")

# ## Initialize doc search object using ScienceDirect and execute search, 
# #   retrieving all results
# doc_srch = ElsSearch("star trek vs star wars",'sciencedirect')
# doc_srch.execute(client, get_all = False)
# print ("doc_srch has", len(doc_srch.results), "results.")