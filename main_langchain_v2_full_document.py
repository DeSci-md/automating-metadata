"""
Use of openai plus langchain for processing information in a pdf
"""
from dotenv import load_dotenv, find_dotenv  # loading in API keys

from langchain.document_loaders import PyPDFLoader  # document loader import
from langchain.chat_models import ChatOpenAI  # LLM import
from langchain import LLMChain  # Agent import
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts.chat import (  # prompts for designing inputs
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)


# Load in API keys from .env file
load_dotenv(find_dotenv())


# Define the PDF document, load it in, convert to raw text, and split into chunks
loader = PyPDFLoader("Zou et al_2013_ZnO nanorods on reduced graphene sheets with excellent field emission, gas.pdf")
document = loader.load()


# Queries, questions for document
query_title = "What is the title of the paper?"
query_authors = "Who are the authors of this paper?"
query_materials = "What materials and chemicals are used by the authors in this work? List all the components in a comma separated list, for example: material A, chemical B, etc."
query_methods = "what are the experimental methods and techniques used by the authors?"
query_motivation = "What is the scientific question or challenge that the authors are trying to address?"
query_future = "What future work or questions are mentioned by the authors?"


# Define language model to use
llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0)  # using for larger token limit


# Structured Output Schema
title_schema = ResponseSchema(name="title", description="This is the publication title of the paper.")
authors_schema = ResponseSchema(name="authors", description="This is a list of the names of the authors of the paper.")
motivation_schema = ResponseSchema(name="motivation", description="This is the question or challenge that the work of this paper seeks to address.")
methods_schema = ResponseSchema(name="methods", description="This is the experimental methods and characterization techniques used by the authors in this paper.")
materials_schema = ResponseSchema(name="materials", description="These are chemicals or materials used by the authors to carry out the work in the paper.")
future_work_schema = ResponseSchema(name="future", description="This is any remaining questions or future work described by the authors in the Conclusions section of the paper.")


# Defining system and human prompts with variables
system_template = "You are a scientific researcher reading the following publication text: {doc_text}."
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)  # providing the system prompt

human_template = "{query}. {format_instructions}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chain = LLMChain(llm=llm, prompt=chat_prompt)


# Asking questions and storing outputs
# Title
response_schema = [title_schema]
output_parser = StructuredOutputParser.from_response_schemas(response_schema)
format_instructions = output_parser.get_format_instructions()

out = chain.run(doc_text=document, query=query_title, format_instructions=format_instructions)
title_dict = output_parser.parse(out)
print("Title prompt done")

# Authors
response_schema = [authors_schema]
output_parser = StructuredOutputParser.from_response_schemas(response_schema)
format_instructions = output_parser.get_format_instructions()

out = chain.run(doc_text=document, query=query_authors, format_instructions=format_instructions)
authors_dict = output_parser.parse(out)
print("Authors prompt done")

# Materials
response_schema = [materials_schema]
output_parser = StructuredOutputParser.from_response_schemas(response_schema)
format_instructions = output_parser.get_format_instructions()

out = chain.run(doc_text=document, query=query_materials, format_instructions=format_instructions)
materials_dict = output_parser.parse(out)
print("Materials Done")

# Methods
response_schema = [methods_schema]
output_parser = StructuredOutputParser.from_response_schemas(response_schema)
format_instructions = output_parser.get_format_instructions()

out = chain.run(doc_text=document, query=query_methods, format_instructions=format_instructions)
methods_dict = output_parser.parse(out)
print("Methods done")

# Motivation
response_schema = [motivation_schema]
output_parser = StructuredOutputParser.from_response_schemas(response_schema)
format_instructions = output_parser.get_format_instructions()

out = chain.run(doc_text=document, query=query_motivation, format_instructions=format_instructions)
motive_dict = output_parser.parse(out)
print("Motive done")

# Future
response_schema = [future_work_schema]
output_parser = StructuredOutputParser.from_response_schemas(response_schema)
format_instructions = output_parser.get_format_instructions()

out = chain.run(doc_text=document, query=query_future, format_instructions=format_instructions)
future_dict = output_parser.parse(out)
print("Future Done")

total_out = title_dict | authors_dict | materials_dict | methods_dict | motive_dict | future_dict  # combining dictionaries together


# Printing outputs
print(f"Response as dict: {total_out}")

print("Title = ", total_out['title'])
print("Authors = ", total_out['authors'])
print("Motivation = ", total_out['motivation'])
print("Methods = ", total_out['methods'])
print("Materials = ", total_out['materials'])
print("Future = ", total_out['future'])

# TODO: Incorporate vector stores/databases, reduce having to analyze the entire document for each question to only the relevant sections
# TODO: Figure out how to filter the reference text out of the input prior to similarity search, avoid having it clog the returned document chunks