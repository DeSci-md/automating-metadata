"""
Script for extracting machine readable text from a web publication/paper which
needs to be downloaded
Adapted from the process described by Wang et. al. 2022 10.1038/s41524-021-00687-2

Elsevier API info: https://dev.elsevier.com/documentation/FullTextRetrievalAPI.wadl
elsapy package info: https://github.com/ElsevierDev/elsapy/blob/master/exampleProg.py
https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/
"""
import json  # for reading in config file for elsevier API key

import httpx  # making web requests
import time

from bs4 import BeautifulSoup  # parsing xml


#%% Use of Elsevier API for obtaining machine readable text (i.e. XML files) for
# online publications
with open("config.json") as file:  # load config/api key
    config = json.load(file)
    api_key = config['apikey']


# https://stackoverflow.com/questions/69190605/how-to-use-elsevier-article-retrieval-api-to-get-fulltext-of-paper
def elsevier_request(paper_doi,apikey):

    client = httpx.Client()

    view ="FULL"

    # format = 'application/json'
    format = 'text/xml'

    url = f"https://api.elsevier.com/content/article/doi/{paper_doi}?APIKey={apikey}&httpAccept={format}&view={view}"
    
    r=client.get(url)

    print(f"Client status: {r}")

    return r

# export the xml file (if found) to a file
# preparse the xml into section?

# Get a document's text
r = elsevier_request('10.1016/j.snb.2008.10.030', api_key)

data = BeautifulSoup(r.text, "xml")

# write the entire xml to file
with open('xml_example.xml', 'w', encoding='UTF-8') as f:
    f.write(data.prettify())


# Pull data from the text
# Get names of all the paper sections
section_names = []
for i in data.find_all('ce:section-title'):
    section_names.append(i.text)

# abstract
abstract = data.find('dc:description').text

# Journal
journal = data.find('prism:publicationName').text