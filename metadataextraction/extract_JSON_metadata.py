import json

"""
This path is currently local, but eventually could be from Henry's data extractor. 
1. Someone puts in a DOI 
2. That goes to Henry's paper extractor
3. The paper goes here. 
"""
path = "/Users/desot1/Dev/desci/Papageorgiou et al_2017_Mechanical properties of graphene and graphene-based nanocomposites.json"

# Open the JSON file
with open('path', 'r') as f:
    data = json.load(f)
    file = f.readlines()

#####BASIC METADATA######
#this ends up printing out a dictionary of all the info. 
meta = data["full-text-retrieval-response"]['coredata']

#Create a JSON file (Should we switch this to JSON-LD?)
with open("metadata.json", "w") as write_file:
    json.dump(meta, write_file, indent=4)

