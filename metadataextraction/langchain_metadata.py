#from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyMuPDFLoader
from langchain.indexes import VectorstoreIndexCreator
import fitz #pdf reading library
import json
import sys 
import os
sys.path.append(os.path.abspath("/Users/desot1/Documents/GitHub/automating-metadata/PDFDataExtractor/pdfdataextractor"))

#from PDFDataExtractor.pdfdataextractor.demo import *
from demo import read_single

os.environ['OPENAI_API_KEY']     

def pdfMetadata(filepath): 
    """
    This returns basic descriptive metadata for the PDF. 

    VARS: 
        Filepath: the path of the file you want to upload. 

    RETURNS: 
        metadata: This is the basic function of the Fitz library. 
        It scrapes the PDF for any embedded metadata. 
    """
    doc = fitz.open(filepath)
    metadata = doc.metadata
        
    #format, encryption, title, author, subject, keywords, creator, producer, creationDate, modDate, trapped
    
    secondary = read_single(filepath)
    
    #there's a chance that these never evaluate to false. Unsure why that is 
    if metadata['author'] == '' and secondary['author'] != '': 
        metadata['author'] == secondary['author']
        
    del secondary['author']

    if metadata['keywords'] == '' and secondary['keywords'] != '': 
        metadata['keywords'] == secondary['keywords']

    del secondary['keywords']
        
    metadata.update(secondary) 
    
   # if metadata['author'] == 'null': 
        #metadata['author'] == read.read_file(filepath)

    return metadata 

def contentmetadata(document, topics):
    contentMetadata = {}

    index = VectorstoreIndexCreator().from_loaders([document])

    for i in range(len(topics)):
        query = "what is the {} of this paper?".format(topics[i])
        contentMetadata[topics[i]] = index.query(query)

    return contentMetadata
     
def metadata(filepath):

    loader = PyMuPDFLoader(filepath)

    categories = ["names given", "university of the author(s)"]# ['Research Question', 'Alterative Approaches', 'Hypothesis', 'Methodology', 'Results', 'Inferences']

    #content = contentmetadata(loader, categories)

    descriptive = pdfMetadata(filepath)
    metadata = descriptive
    """metadata = [descriptive, content]
    
    with open("metadata.json", "w") as write_file:
        json.dump(metadata, write_file, indent=4)  

    print(metadata)
"""
    return metadata

