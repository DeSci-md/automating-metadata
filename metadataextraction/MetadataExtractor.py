#setup 
import openai as openai #Extracting content metadata
import fitz #pdf reading library
import time #to ensure we don't call too often from openai
from bs4 import BeautifulSoup #to extract XML info -> will be eliminated eventually
import matplotlib.pyplot as plt
import numpy as np 
import math
import json

# Library to import pre-trained model for sentence embeddings
from sentence_transformers import SentenceTransformer

# Calculate similarities between sentences
from sklearn.metrics.pairwise import cosine_similarity

# package for finding local minimas
from scipy.signal import argrelextrema



def splitXMLParagraphs(filepath):
    """
    This is partially a dummy function. This extraction is limited by the fact that XML isn't standard. 
    However, I want to start parsing and iterating over txt using GPT as a way of mechanizing/beginning to evaluate our 
    thoughts on how to gain greater info about these papers. 


    """
    with open(filepath, 'r') as f:
        data = f.read()

    # Passing the stored data inside
    # the beautifulsoup parser, storing
    # the returned object
    Bs_data = BeautifulSoup(data, "xml")
    para = Bs_data.find_all('p')
    paragraphs = []

    for x in range(len(para)): 
        if len(para[x].text) < 2800:
            paragraphs.append(para[x].text)
        else: 
            para[x.text].split
            x -= 1
    return paragraphs

def pdfMetadata(filepath, fitz): 
    doc = fitz.open(filepath)
    metadata = doc.metadata
    return metadata 


def splitPDFparagraphs(fname,filepath, fitz): 
    doc = fitz.open(filepath)  # open document
    out = open(fname + ".txt", "wb")  # open text output
    for page in doc:  # iterate the document pages
        text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
        out.write(text)  # write text of page
        out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
    out.close()

def pdfTextExtraction(filename, filepath): 
    doc = fitz.open(filepath)  # open document
    with open(filename + '.txt', 'w') as out:
        for page in doc:  # iterate the document pages
            text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
            out.write(text.decode('utf-8'))  # write text of page
            out.write(bytes((12,)).decode('utf-8'))  # write page delimiter (form feed 0x0C) 
    
#limitation -> recipe for paragraph extraction, but not necessarily basic metadata like authors etc
def contentMetadataRecipe(openai, filename, prompt): 
# Imports GPT3 model. Using davinci at the moment for final outputs. Curie for testing. 
    counter = 0
    res = ""
    ans = []
    #Wondering if we can retrieve the model earlier on -> so we don't have to do this multiple times. 
    #openai.Model.retrieve("text-curie-001")
    openai.Model.retrieve("text-curie-001")
    
    with open(filename, 'r') as f: 
        paragraphs = f.readlines()

    # structures the base prompt for the model
    #TO BE UPDATED. I want to train my own version of this. 
    #base_prompt = "Paragraph:So yeah, do you see in those ecosystems really cool as pop in? Lots of cool projects, many more I forgot a bunch, but yeah, Jocelyn is always curating this cool landscape, so just check it out. I have the Twitter right there. And yeah, so we just heard about it. So sharing scientific data is super important. Why? Because, well, if we share data, we can collaborate much more easily. We can build bigger data sets and bigger data sets means more statistical power, reliable results, right? So that's pretty cool. And it also means more access to the data that, so there's not the same access to cool instruments that help you with data collection across labs. So if you're in an underfunded research institution, you just may not have the ability to collect the same type of data that a well-funded institution may have. So if we all share data, we all have better access to make cool scientific discoveries. So that's pretty cool, right? But also sharing scientific data right now. It's pretty expensive, it's pretty vulnerable because it's stored on centralized databases where we just have to trust that they keep the database running. It's also not rewarded. So currently, what counts in science is having your PDF cited, but it doesn't matter if you make your data accessible, like you just cannot accrue credit to it. Or there's some ways you can, but it's just not really easy. And it's also pretty painful. So there's a couple of repos out there where you can store your data. These are funded by some governmental institutions. There you access not great. And then also, if you want to find the data, you need to know which repo it's stored at. So you need to find the repo. Then you need to find the data. It's all, it's a hassle, so it's not great.\nExample Summary:Sharing scientific data is important as it allows for better collaboration, bigger data sets, reliable results, and better access for researchers in underfunded institutions. However, currently sharing data is expensive, vulnerable, and not rewarded. It is stored on centralized databases which requires that we trust those servers to keep running. Also, there are no incentives for for making the data accessible. Currently, the only way that we can give credit for using someone else's work is citing their PDF. But with PDF citations, it doesn't matter if you make your data accessible. Sharing data right now isn't worth the cost and time for the researcher.\nParagraph:"

    base_prompt = "Does this paragraph describe the paper's " + prompt + "Answer with a Yes or No."
    
    for x in range(len(paragraphs)): 
        if len(paragraphs[x]) > 100: 
            thought = paragraphs[x].strip()
            p = base_prompt + thought
        else: 
            continue
        
        print('I enter the loop when my paragraph is as tiny as:' +str(len(paragraphs[x])))
        # Model parameters were determined through sandbox testing. Temp is fairly high to allow the model
        response = openai.Completion.create(
            #model = "text-curie-001",
            model="text-curie-001",
            prompt = p,
            max_tokens=400,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5
        )
        answer = response["choices"][0]["text"]
        ans.append(answer)
        
        if answer.find("Yes") != -1: 
            question = "What is the paper's" + prompt + "?" + thought
            # Model parameters were determined through sandbox testing. Temp is fairly high to allow the model
            response2 = openai.Completion.create(
                #model = "text-curie-001",
                model="text-curie-001",
                prompt = question,
                max_tokens=400,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )
            res += response2["choices"][0]["text"]    
        
        
        counter+=1
        #print(counter)
        # A sleep counter because microsoft keeps limiting my creativity
        if counter%30==0 and counter!=0:
            print("\n\n\nI am so sleepy\n\n\n")
            time.sleep(60)
        
        if len(res) < 1600: 
            final = "Summarize these responses into one sentence that tells me the paper's" + prompt + "\n" + res
            response3 = openai.Completion.create(
                        #model = "text-curie-001",
                        model="text-curie-001",
                        prompt = final,
                        max_tokens=400,
                        temperature=0.7,
                        top_p=1,
                        frequency_penalty=0.5,
                        presence_penalty=0.5
                )
        else:
            modular = res.split('.')
            for i in range(len(modular)): 
                if i< len(modular)/2:
                    res1 += modular[i]
                else:
                    res2 += modular[i]
            
            if len(res1) < 1600: 
                final = "Summarize this responses into one sentence that tells me the paper's" + prompt + "\n" + res1
                response4 = openai.Completion.create(
                            #model = "text-curie-001",
                            model="text-curie-001",
                            prompt = final,
                            max_tokens=400,
                            temperature=0.7,
                            top_p=1,
                            frequency_penalty=0.5,
                            presence_penalty=0.5
                    )
            if len(res2) < 1600: 
                final = "Summarize this responses into one sentence that tells me the paper's" + prompt + "\n" + res2
                response5 = openai.Completion.create(
                            #model = "text-curie-001",
                            model="text-curie-001",
                            prompt = final,
                            max_tokens=400,
                            temperature=0.7,
                            top_p=1,
                            frequency_penalty=0.5,
                            presence_penalty=0.5
                    )

    return(response3)


def main(): 
    """
    A potential combo of the functions above to get a set of metadata out. 
    """
    openai.api_key = "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"

    filename = 'Papageorgiou et al_2017_Mechanical properties of graphene and graphene-based nanocomposites'

    filepathpdf = "/Users/desot1/Dev/desci/Papageorgiou et al_2017_Mechanical properties of graphene and graphene-based nanocomposites.pdf"
    
    text = pdfTextExtraction('Papageorgiou et al_2017_Mechanical properties of graphene and graphene-based nanocomposites.txt', filepathpdf)
    
    filepathtxt = filename + '.txt'

    descriptiveMetadata = pdfMetadata(filepathpdf)
    
    contentMetadata = {}


    categories = ['Research Question', 'Alterative Approaches', 'Hypothesis', 'Methodology', 'Results', 'Inferences']
    
    #paragraphs = splitXMLParagraphs(filepathxml)
    contentMetadata['Research Question'] = 'this is the research question'


    for i in range(len(categories)):
        print(contentMetadata)

        contentMetadata = {categories[i]: contentMetadataRecipe(openai, filepathtxt, categories[i])}
        
    print(contentMetadata)

    metadata = [contentMetadata, descriptiveMetadata]

    with open("metadata.json", "w") as write_file:
        json.dump(metadata, write_file, indent=4)  


if __name__ == "__main__": 
    main()    

