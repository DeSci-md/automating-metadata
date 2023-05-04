from flask import Flask, Blueprint, jsonify
import json
from habanero import Crossref, cn
import httpx
from markupsafe import escape

search_bp = Blueprint('search_flask', __name__)

@search_bp.route('/')
def home():
    x = "<p>Home page, input a doi number to search via /doisearch/[doi number] in the address bar.</p><p>Input the DOI with all slashes replaced with hyphens (-), may be a way to avoid this in the future.</p>"

    return x

@search_bp.route('/doisearch/<doi_number_hyphen>')
def doi_search(doi_number_hyphen):
    """
    Use the user inputted DOI identifier and perform a search for published data and text
    using API calls to Semantic Scholar, Elsevier, and Crossref
    """
    print(doi_number_hyphen)
    doi_number = doi_number_hyphen.replace('-','/')
    print(doi_number)
    print(type(doi_number))

    return paper_data_json_single(doi_number)

def paper_data_json_single(doi):
    """
    Create a json output file for a single paper using the inputed identifier.
    Only using a DOI string at the moment
    File constructed based on the info in metadata_formatting_categories.md

    Inputs:
    doi - string, DOI string for the paper/publication of interest
    output - string, path of where to save json output
    ---
    output:
    dictionary, conversion to json and writing to file
    """
    #%% Setting up info for usage of API's
    # define crossref object
    cr = Crossref()  
    cr.mailto = 'haloh@mix.wvu.edu'
    cr.ua_string = 'Python script for retrieving paper info from query for research.'

    # Elsevier API key
    with open("config.json") as file:  # load config/api key
        config = json.load(file)
        apikey = config['apikey']

    client = httpx.Client()


    #%% Info from Crossref
    r = cr.works(ids = f'{doi}')  # Crossref search using DOI, "r" for request

    title = r['message']['title'][0]
    type = r['message']['type']
    pub_name = r['message']['container-title'][0]
    pub_date = r['message']['published']['date-parts'][0]
    subject = r['message']['subject']

    inst_names = []  # handling multiple colleges, universities
    authors = []  # for handling multiple authors

    for i in r['message']['author']:
        authors.append(i['given'] + ' ' + i['family'])
        try:
            name = (i['affiliation'][0]['name'])
            if name not in inst_names:
                inst_names.append(name)
        except:
            continue

    refs = []
    for i in r['message']['reference']:
        try:
            refs.append(i['DOI'])
        except:
            refs.append(f"{i['key']}, DOI not present")
        
    url_link = r['message']['URL']
    

    #%% Info from Elsevier
    format = 'application/json'
    view ="FULL"
    url = f"https://api.elsevier.com/content/article/doi/{doi}?APIKey={apikey}&httpAccept={format}&view={view}"
    with httpx.Client() as client:
        r=client.get(url)
    
    json_string = r.text
    d = json.loads(json_string)  # "d" for dictionary

    try:
        d['full-text-retrieval-response']
        scopus_id = d['full-text-retrieval-response']['scopus-id']
        abstract = d['full-text-retrieval-response']['coredata']['dc:description']

        keywords = []
        for i in d['full-text-retrieval-response']['coredata']['dcterms:subject']:
            keywords.append(i['$'])

        original_text = d['full-text-retrieval-response']['originalText']
    except:
        print(f"Elsevier text retieval bad for {doi}")
        scopus_id = 'None, elsevier error'
        abstract = 'None, elsevier error'
        keywords = ['None, elsevier error']
        original_text = 'None, elsevier error'
    

    #%% Info from Semantic Scholar
    url = f'https://api.semanticscholar.org/graph/v1/paper/{doi}/?fields=fieldsOfStudy,tldr,openAccessPdf'
    with httpx.Client() as client:
        r = client.get(url)

    json_string = r.text
    d = json.loads(json_string)

    paper_id = d['paperId']
    field_of_study = []
    if d['fieldsOfStudy'] is None:
        field_of_study = 'None'
    else:
        for i in d['fieldsOfStudy']:
            field_of_study.append(i)
    if d['tldr'] is None:
        tldr = 'None'
    else:
        tldr = d['tldr']
    
    if d['openAccessPdf'] is None:
        openaccess_pdf = 'None'
    else:
        openaccess_pdf = d['openAccessPdf']['url']


    #%% Constructing output dictionary
    output_dict = {
        'DOI':doi,
        'scopus_id':scopus_id,
        'paperId':paper_id,
        'title':title,
        'publication_name':pub_name,
        'publish_date':pub_date,
        'type':type,
        'keywords':keywords,
        'subject':subject,
        'fields_of_study':field_of_study,
        'authors':authors,
        'institution_names':inst_names,
        'references':refs,
        'tldr':tldr,
        'abstract':abstract,
        'original_text':original_text,
        'openAccessPdf':openaccess_pdf,
        'URL_link':url_link 
    }

    return output_dict